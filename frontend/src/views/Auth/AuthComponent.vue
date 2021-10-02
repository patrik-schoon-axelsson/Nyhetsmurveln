<template>
<div>
    <Logout v-if="user" /> 
    <Login v-else />
</div>
</template>

<script>
import { mapState } from 'vuex';
import Login from './Login.vue';
import Logout from './Logout.vue';

export default {
  components: { Login, Logout },
    computed: mapState({
        user: state => state.auth.user,
        token: state => state.auth.token
    })
}
</script>

<style>

</style>