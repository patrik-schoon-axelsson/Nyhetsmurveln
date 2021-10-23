import { createApp } from 'vue'
import './assets/scss/main.scss'
import 'material-design-icons/iconfont/material-icons.css'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
