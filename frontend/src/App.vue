<template>
  <div v-if="feedLoading">
    <h1 class="center-align">LADDAR NYHETER...</h1>
  </div>
  <div id="main-app" v-else>
    <NavBar />
    <div class="container">
      <div class="row">
        <ul class="tabs" id="tabs" v-if="feeds">
          <li class="tab col s3" v-for="feed in feeds" :key="feed._id.$oid">
            <router-link :to="{ name : 'Feeds', params : { id: feed._id.$oid }}">{{feed.title}}</router-link>
          </li> 
        </ul>  
        <router-view :key="this.$route.params.id" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import M from 'materialize-css';
import './components/Nav/NavBar.vue'
import store from './store'
import NavBar from './components/Nav/NavBar.vue'

export default {
  components: { NavBar },
  data() {
    return {
      feeds: null,
      feedLoading: false
    }  
  },
  mounted() {

    // JWT localstorage refreshtoken
    const jwt_token = window.localStorage.getItem('jwt')

    if (jwt_token) {
      this.$store.dispatch('refreshToken')
    }

    M.AutoInit();
    
    this.feedLoading = true;
  
    axios.get("/api/feeds")
    .then((feeds) => {
      this.feeds = feeds.data
    })
    .catch(err => console.log(err))
    .finally(() => {
      this.feedLoading = false
      
      this.$store.dispatch('setFeedsOnLoad', this.feeds)
    })
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
