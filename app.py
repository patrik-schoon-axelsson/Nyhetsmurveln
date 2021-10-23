import os
import datetime
from dotenv import load_dotenv
from mongoengine.errors import NotUniqueError, ValidationError
from models import User, Feed
from werkzeug.security import check_password_hash, generate_password_hash
from feedparser.api import parse
from flask import Flask, json, request, jsonify
from flask_mongoengine import MongoEngine
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager
import feedparser

load_dotenv()

app = Flask(__name__, 
            static_folder='frontend/dist/', 
            static_url_path="/")
            
app.config["JWT_SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

# Flask-JWT-extended setup

jwt = JWTManager(app)

# MongoDB-setup

app.config['MONGODB_SETTINGS'] = {
    "db": "nyhetsmurveln",
    "host": os.environ["MONGO_URI"],
    # Required for deployment, or there's a connection error due to PyMongo 3
    "connect": False
}

db = MongoEngine(app)

@app.route("/api/register", methods=['POST'])
def register():
    hashed_pw = generate_password_hash(password=request.json["password"])
    user = User(email=request.json["email"], password=hashed_pw )
    user.save()

    return jsonify(user)    

@app.route("/api/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    refreshed_token = create_access_token(identity=identity)

    return jsonify(token=refreshed_token, user=identity)

@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]

        user = User.objects().get_or_404(email=email)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        # Returned to the client, so removing unneccesary info like password hash, ID etc
        sanitized_user = {
            "email": user.email,
            "isAdmin": user.isAdmin,
            "subscriptions": user.subscriptions
        }

        if check_password_hash(user.password, password):
            return jsonify(token=access_token, refreshToken=refresh_token, user=sanitized_user)
        else:
            return jsonify({
                "status": 401,
                "message": "Either the password or the email was incorrect"
            }), 401
    except KeyError:
        return jsonify({
            "status": 403,
            "message": "Request not accepted. This endpoint accepts JSON with the keys password and username."
        }), 403

# Route for handling account changes, by authenticated users.
@app.route("/api/users", methods=["PUT", "POST"])
@jwt_required()
def user_update():
    # PUT handles updates to password and subscriptions, POST handles adding and removing subscriptions.
    user = json.loads(get_jwt_identity())
    db_user = User.objects.get(id=user["_id"]["$oid"])

    if request.method == "PUT":
        return "Updates"
    elif request.method == "POST":
        return "Added subscription!"

# The Feedparser API. Accepts object ID strings, URL taken from the database of
# a valid RSS or Atom feed, with error handling for invalid URLs, faulty JSON content
# etc.

@app.route("/api/parser/<feed_id>", methods=['POST'])
def api_parser(feed_id):
    # Obviously we do not want the feedparser endpoint exposed to accept "pure"
    # URL-values, or we'll end up DDOSing half the RSS feeds on the planet.
    # Instead, we accept document-IDs as a URL parameter and get the URL from Mongo.

    try:
        url = json.loads(Feed.objects().get_or_404(id=feed_id).to_json())["url"]
        feed = feedparser.parse(url)
        if len(feed.entries) > 0:
            return jsonify({
                    "status": 200,
                    "message":  "Feed accepted and parsed.",
                    "entries": feed.entries,
                    "feed": feed.feed
                })
        else:
            return jsonify({
                "status": 403,
                "message": "Invalid URL. Could not parse. Make sure the URL is a valid RSS or Atom feed."
            }), 403
    except KeyError:
            return jsonify({ 
                "status": 404,
                "message": "Request lacks the url key. This endpoint accepts only JSON with a key labelled url."
                }), 404

@app.route("/api/feeds/<doc_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required(optional=True)
def feeds_single(doc_id):
    try:
        feed = Feed.objects.get(id=doc_id)
    except ValidationError as e:
        return jsonify({
            "status": 404,
            "message": f"Invalid query. This endpoint only accepts valid MongoDB ObjectID strings. {e} is not an acceptable query-string.."
        }), 404
    user = get_jwt_identity()
    # Sets a admin-status variable only if there is a jwt identity, to avoid typeerror cases.
    if user:
        admin_status = json.loads(User.objects.get(id=user["_id"]["$oid"]).to_json())["isAdmin"]

    if request.method == "PUT":
        if user and admin_status:
            feed.update(title=request.json["title"] , url=request.json["url"], description=request.json["description"], added_by=User.objects.get_or_404(id=user["_id"]["$oid"]))
            
            return jsonify({
                "status": 200,
                "message": f"Updated object with id: {doc_id}"
            })
        else:
            return jsonify({
                "status": 401,
                "message": "You need to login to perform a PUT request on this endpoint."
            })
    elif request.method == "DELETE":
                if user and admin_status:
                    feed.delete()

                    return jsonify({
                        "status": 200,
                        "message": f"Deleted item with id: {doc_id} succesfully."
                    })
                else:
                    return jsonify({
                        "status": 401,
                        "message": "You need to login to perform a DELETE request on this endpoint."
                    })
    else:
        return feed.to_json()

@app.route("/api/feeds", methods=["GET", "POST"])
@jwt_required(optional=True)
def feeds_all():
    user = get_jwt_identity()

    if request.method == "POST":
        if user:
            # For security, check if isAdmin is verifiably true from the DB on the user object:
            # A little inelegant, but functional for prototyping.

            admin_status = json.loads(User.objects.get(id=user["_id"]["$oid"]).to_json())["isAdmin"]

            if admin_status:
                try:
                    feed = Feed(title=request.json["title"] , url=request.json["url"], description=request.json["description"], added_by=user["_id"]["$oid"])
                    feed.save()
                except NotUniqueError as e:
                    return jsonify({
                        "error": 403,
                        "message": f"There is a duplicate entry in the database, with either the same title or URL. Please delete the duplicate item or update the original. Details of duplicate entries: {e}"
                    })
                except KeyError as e:
                    return jsonify({
                        "error": 403,
                        "message": f"Invalid document error, KeyError raised because request lacks the field {e}. This endpoint allows the following keys: title: <string>, url: <string>, description: <string>. Please adjust and try again."
                    })
                except:
                    return jsonify({
                        "error": 500,
                        "message": "Unexpected server issue! Please contact the administrator."
                    })

                req_user = {
                    "id": user["_id"]["$oid"],
                    "email": user["email"],
                    "admin": user["isAdmin"],
                    "subscriptions": user["subscriptions"]
                    }

                return jsonify({
                    "user": req_user,
                    "status": 200,
                    "message": "Added new feed.",
                    "feed": feed.to_json()
                })
            elif not admin_status:
                return jsonify({
                    "error": 403,
                    "message": "Request denied, your account is not an administrator account. If this is mistaken, contact the administrator."
                })
        else:
            return jsonify({
                "error": 401,
                "message": "No bearer token present in request. Request denied. Try logging in again."
            })
    elif request.method == "GET":
        return Feed.objects.all().to_json()


# Catch-All route for serving the static site.
  
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run()