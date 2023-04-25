import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import { stringFunctions } from '@/globalFunctions.js'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

const app = createApp(App)
app.config.globalProperties.$stringFunctions = stringFunctions
app.use(router)
app.mount('#app')
