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

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

# Flask-JWT-extended setup

jwt = JWTManager(app)

# MongoDB-setup

app.config['MONGODB_SETTINGS'] = {
    "db": "nyhetsmurveln",
    "host": os.environ["MONGO_URI"]
}

db = MongoEngine(app)

@app.route("/api/register", methods=['POST'])
@jwt_required(refresh=True)
def register():
    hashed_pw = generate_password_hash(password=request.json["password"])
    user = User(email=request.json["email"], password=hashed_pw )
    user.save()

    return jsonify(user)    

@app.route("/api/refreshtoken", methods=["POST"])
def refresh_token():
    identity = get_jwt_identity()
    refreshed_token = create_access_token(identity=identity)

    return jsonify(access_token=refresh_token)

@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]

        user = User.objects.get(email=email)
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        if check_password_hash(user.password, password):
            return jsonify(token=access_token, refreshToken=refresh_token, user=user.to_json())
        else:
            return jsonify({
                "status": 403,
                "message": "Either the password or the email was incorrect"
            })
    except KeyError:
        return jsonify({
            "status": 403,
            "message": "Request not accepted. This endpoint accepts JSON with the keys password and username."
        })

# The Feedparser API. Accepts JSON posts with the url key being the URL of
# a valid RSS or Atom feed, with error handling for invalid URLs, faulty JSON content
# etc.

@app.route("/api/parser", methods=['POST'])
def api_parser():
    try:
        url = request.json["url"]
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
            })
    except KeyError:
            return jsonify({ 
                "status": 404,
                "message": "Request lacks the url key. This endpoint accepts only JSON with a key labelled url."
                })

@app.route("/api/feeds/<doc_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required(optional=True)
def feeds_single(doc_id):
    try:
        feed = Feed.objects.get_or_404(id=doc_id)
    except ValidationError as e:
        return jsonify({
            "status": 404,
            "message": f"Invalid query. This endpoint only accepts valid MongoDB ObjectID strings. {e} is not an acceptable query-string.."
        })
    user = get_jwt_identity()

    if request.method == "PUT":
        if user:
            return "Something!"
        else:
            return jsonify({
                "status": 401,
                "message": "You need to login to perform a PUT request on this endpoint."
            })
    elif request.method == "DELETE":
                if user:        
                    return "Something else!"
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

@app.route("/")
def index():
    return jsonify({"status": 200, "msg": "Hello world! This is where the frontend static will be served!"})

if __name__ == "__main__":
    app.run(debug=True)