<template>
  <nav class="nav-extended">
    <div class="nav-wrapper">
      <router-link to="/" class="brand-logo">Nyhetsmurveln</router-link>
      <a href="#" data-target="mobile-nav" class="sidenav-trigger"><i class="material-icons">menu</i></a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><router-link to="/about">Om Sidan</router-link></li>
        <li><AuthComponent /></li>
      </ul>
    </div>
    <div class="nav-content">
        <div  class="progress" v-if="feedLoading">
            <div class="indeterminate"></div>
        </div>
        <ul class="tabs tabs-transparent" id="tabs" v-if="feeds">
          <li class="tab col s3" v-for="feed in feeds" :key="feed._id.$oid">
            <router-link :to="{ name : 'Feeds', params : { id: feed._id.$oid }}">{{feed.title}}</router-link>
          </li> 
        </ul>  
    </div>
  </nav>

  <!-- Mobile Navbar -->
  <ul class="sidenav" id="mobile-nav">
      <li><router-link to="/about">Om Sidan</router-link></li>
      <li><AuthComponent /></li>
      <li v-for="feed in feeds" :key="feed._id.$oid">
        <router-link :to="{ name : 'Feeds', params : { id: feed._id.$oid }}">{{feed.title}}</router-link>
      </li>
  </ul>
</template>

<script>
import axios from 'axios';
import  NavBar from '@/components/Nav/NavBar.vue'
import AuthComponent from '@/views/Auth/AuthComponent.vue'

export default {
  components: { AuthComponent, NavBar },
    component: {
        AuthComponent
    },
    data(){
      return {
        feedLoading: null,
        feeds: null
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

<style>

</style>