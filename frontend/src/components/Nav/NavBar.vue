<template>
  <nav>
    <div class="nav-wrapper">
      <router-link to="/" class="brand-logo">Nyhetsmurveln</router-link>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><router-link to="/about">Om Sidan</router-link></li>
        <li><AuthComponent /></li>
      </ul>
    </div>
  </nav>
</template>

<script>
import AuthComponent from '@/views/Auth/AuthComponent.vue'

export default {
  components: { AuthComponent },
    component: {
        AuthComponent
    }
}
</script>

<style>

</style>