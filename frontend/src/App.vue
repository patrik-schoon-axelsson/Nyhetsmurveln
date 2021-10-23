<template>
  <div v-if="feedLoading">
    <div class="row">
      <h1 class="center-align">LADDAR NYHETER...</h1>
    </div>
    <div class="row">
      <div class="center-align">
        <div class="preloader-wrapper active">
        <div class="spinner-layer spinner-red-only">
          <div class="circle-clipper left">
            <div class="circle"></div>
          </div><div class="gap-patch">
            <div class="circle"></div>
          </div><div class="circle-clipper right">
            <div class="circle"></div>
          </div>
        </div>
    </div>
    </div>
  </div>
  </div>
  <div id="main-app" v-else>
    <NavBar/>
    <div class="container">
      <div class="row">
        <router-view :key="this.$route.params.id"></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import M from 'materialize-css';
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
html {
  font-size: 14px;
  body {
    font-family: 'Source Code Pro', monospace;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    .headline {
      padding-left: 2rem;
      font-family: 'Indie Flower', cursive;
    }
  }
}
</style>
