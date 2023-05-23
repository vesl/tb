import { createApp } from 'vue'
import { createStore } from 'vuex'
import { stringFunctions } from '@/globalFunctions.js'

import App from './App.vue'
import router from '@/router'

import PrimeVue from 'primevue/config'
import Divider from 'primevue/divider'
import Button from 'primevue/button'

import 'primeicons/primeicons.css'
import "primevue/resources/primevue.min.css"
import "primevue/resources/themes/saga-blue/theme.css"

const store = createStore({
  state () {
    return {
      apis_domain: '.tb.svc.k8s.slav.rocks',
      symbols: [
        'BTCUSDT',
        'VETETH',
        'ETHUSDT'
      ],
      nav: {
        apps: [
          {
            name: 'scrapper',
            icon: 'pi pi-sync',
            views: [
              {
                name: 'klines',
              },
              {
                name: 'talib'
              }
            ]
          },
          {
            name: 'trainer',
            icon: 'pi pi-cog',
            views: [
              {
                name: 'datasets'
              },
              {
                name: 'model',
              },
              {
                name: 'darwin',
              }
            ]
          },
          {
            name: 'trader',
            icon: 'pi pi-money-bill',
            views: [
              {
                name: 'live',
              },
              {
                name: 'paper',
              },
              {
                name: 'backtest',
              }
            ]
          },
        ]
      }
    }
  }
})

const app = createApp(App)
app.config.globalProperties.$stringFunctions = stringFunctions
app.use(router)
app.use(store)
app.use(PrimeVue)
app.component('PrimeDivider',Divider)
app.component('PrimeButton',Button)
app.mount('#app')
