import { createApp } from 'vue'
import { createStore } from 'vuex'
import { stringFunctions } from '@/globalFunctions.js'
import { toastFunctions } from '@/globalFunctions.js'

import App from './App.vue'
import router from '@/router'

import PrimeVue from 'primevue/config'
import ProgressSpinner from 'primevue/progressspinner'
import ToastService from 'primevue/toastservice'
import DataTable from 'primevue/datatable'
import Dropdown from 'primevue/dropdown'
import Divider from 'primevue/divider'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import Card from 'primevue/card'

import 'primeicons/primeicons.css'
import "primevue/resources/primevue.min.css"
import "primevue/resources/themes/arya-blue/theme.css"

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
app.config.globalProperties.$toastFunctions = toastFunctions
app.use(router)
app.use(store)
app.use(PrimeVue)
app.use(ToastService)
app.component('PrimeProgressSpinner',ProgressSpinner)
app.component('PrimeDataTable', DataTable)
app.component('PrimeDropdown', Dropdown)
app.component('PrimeDivider', Divider)
app.component('PrimeColumn', Column)
app.component('PrimeButton', Button)
app.component('PrimeToast', Toast)
app.component('PrimeCard', Card)
app.mount('#app')
