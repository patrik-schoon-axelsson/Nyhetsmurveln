<template>
  <div class="col s12 m6 l4">
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
.card-title {
  font-size: 1.1rem;
}
p {
  font-size: .8rem;
}

img {
  max-width: 100%;
  height: auto; 
}
</style>