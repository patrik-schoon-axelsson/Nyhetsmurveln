<template>
 <div v-if="isLoading">
     <h1> Läser in nyheter... Detta kan ta uppemot 30 sekunder, var god dröj.</h1>
 </div>
 <div v-else class="row"> 
     <h1 v-if="error">{{error}}</h1>
     <hr>
    <div class="col s12 m7" v-if="feed">
    <div class="card medium">
      <div class="card-stacked">
        <div class="card-content">
        <h4 class="header">{{feed.title}}</h4>
          <p class="flow-text">{{feed.subtitle}}</p>
          <hr>
          <p>{{feed.rights}}</p>
        </div>
        <div class="card-action">
          <a :href="feed.link" target="_blank">{{feed.title}} - Extern Länk</a>
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <FeedEntry v-for="entry in entries" :key="entry.id" :entry="entry" />
  </div>
 </div>
</template>

<script>
import axios from 'axios'
import FeedEntry from './Feeds/FeedEntry.vue'

export default {
    components: {
      FeedEntry
    },
    data(){
        return {
            isLoading: false,
            entries: null,
            feed: null,
            error: null
        }
    },
    mounted(){
        this.isLoading = true;

        axios.post(`/api/parser/${this.$route.params.id}`)
        .then((feed_item) => {

            console.log(feed_item.status)

            if(feed_item.data.status == 403) {
                return this.error = feed_item.data.message
            }
            this.feed = feed_item.data.feed;
            this.entries = feed_item.data.entries;
        })
        .catch(err => this.error = err)
        .finally(
            this.isLoading = false
        )
    },
    watch: {
        $route (to, from) {

        }
    },
}
</script>

<style scoped>

</style>