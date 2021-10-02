<template>
<!-- Modal Trigger -->
  <a class="modal-trigger" href="#logout_modal">Logga Ut</a>
  <!-- Modal Structure -->
<teleport to="body">
    <div id="logout_modal" class="modal">
    <form @submit.prevent="logout">
      <div class="modal-content">
            <button type="submit" class="btn modal-close">Logga Ut</button>
        </div>
        <div class="modal-footer">
            <a href="#!" class="modal-close waves-effect waves-green btn-flat">Stäng</a>
        </div>
    </form>
    </div>
</teleport>
</template>

<script>
export default {
    methods: {
        logout() {
            this.$store.dispatch('logoutUser')
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