<template>
<!-- Modal Trigger -->
  <a class="modal-trigger" href="#login_modal">Logga In</a>
  <!-- Modal Structure -->
<teleport to="body">
    <div id="login_modal" class="modal">
        <form @submit.prevent="login">
        <div class="modal-content">
        <label for="email">Email: </label>
        <input name="email" v-model="email" type="email">
        <label for="password">Password: </label>
        <input name="password" v-model="password" type="password">        
        </div>
        <div class="modal-footer">
            <a href="#!" class="modal-close waves-effect waves-green btn-flat">Stäng</a>
            <button class="btn" type="submit modal-close">Logga in</button>
        </div>
        </form>
    </div>
  </teleport>
</template>

<script>
import M from 'materialize-css'

export default {
    data() {
        return {
            email: '',
            password: '',
        }
    },
    methods: {
        login(){
            const credentials = {
                email: this.email,
                password: this.password
            }

            this.$store.dispatch('loginUser', credentials)
        }
    },
    mounted() {
        const elems = document.querySelectorAll('.modal');

        M.Modal.init(elems)
    }
}
</script>

<style>

</style>