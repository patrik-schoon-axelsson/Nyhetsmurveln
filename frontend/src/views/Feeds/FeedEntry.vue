<template>
  <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">{{entry.title}}</span>
          <p v-html="entry.summary"></p>
        </div>
        <div class="card-action">
          <a :href="entry.link" target="_blank">Extern Länk</a>
        </div>
      </div>
    </div>
</template>

<script>
export default {
    props: [ 'entry' ]
}
</script>

<style>

img {
  max-width: 100%;
  height: auto; 
}
</style>