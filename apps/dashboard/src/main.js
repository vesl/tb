import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import { stringFunctions } from '@/globalFunctions.js'
import { createStore } from 'vuex'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

const store = createStore({
  state () {
    return {
      symbols: [
        'BTCUSDT',
        'VETETH',
        'ETHUSDT'
      ],
      apis_domain: '.tb.svc.k8s.slav.rocks'
    }
  }
})

const app = createApp(App)
app.config.globalProperties.$stringFunctions = stringFunctions
app.use(router)
app.use(store)
app.mount('#app')
