import axios from 'axios';
import M from 'materialize-css'


const AuthStore = {
    state: () => ({
        token: '',
        user: null,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${AuthStore.state.token}`},
    }),
    mutations: {
        setToken(state, token) {
            state.token = token
        },
        setUser(state, user) {
            state.user = user
        }
    },
    actions: {
        loginUser(context, payload) {
            const email = payload.email
            const password = payload.password

            axios.post('/api/login', { email: email, password: password })
            .then((res) => {
            
                window.localStorage.setItem('jwt', res.data.refreshToken)
                context.commit('setToken', res.data.token)
                context.commit('setUser', res.data.user)
            })
            .catch(err => M.toast({html: `${err}`}))
        },
        logoutUser(context) {
            
            window.localStorage.removeItem('jwt')
            context.commit('setToken', null)
            context.commit('setUser', null)
        },
        refreshToken(context, refreshToken) {
            
            axios.post('/api/refreshtoken', { refreshToken: refreshToken},{ headers: { Authorization: `Bearer ${window.localStorage.getItem('jwt')}` }})
            .then(res => {

                context.commit('setToken', res.data.token)
                context.commit('setUser', res.data.user)                
            })
            .catch(err => console.log(err))
        }
    }
}

export default AuthStore