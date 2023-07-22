import { createApp } from 'vue'
import { createStore } from 'vuex'
import { string } from '@/globalFunctions.js'

import App from './App.vue'
import router from '@/router'

import VueCookies from 'vue-cookies'
import PrimeVue from 'primevue/config'
import ProgressSpinner from 'primevue/progressspinner'
import AccordionTab from 'primevue/accordiontab'
import ToastService from 'primevue/toastservice'
import InputNumber from 'primevue/inputnumber'
import InputSwitch from 'primevue/inputswitch'
import InputText from 'primevue/inputtext'
import Accordion from 'primevue/accordion'
import DataTable from 'primevue/datatable'
import Dropdown from 'primevue/dropdown'
import Calendar from 'primevue/calendar'
import TabPanel from 'primevue/tabpanel'
import TabView from 'primevue/tabview'
import Divider from 'primevue/divider'
import Avatar from 'primevue/avatar'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Badge from 'primevue/badge'
import Toast from 'primevue/toast'
import Chart from 'primevue/chart'
import Chip from 'primevue/chip'
import Card from 'primevue/card'
import Tag from 'primevue/tag'

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
      periods: [
        'live',
        'historical'
      ],
      nav: {
        apps: [
          {
            name: 'scrapper',
            icon: 'pi pi-sync',
            views: [
              {
                name: 'klines'
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
                name: 'models'
              },
              {
                name: 'darwin'
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
app.config.globalProperties.$string = string
app.use(router)
app.use(store)
app.use(PrimeVue)
app.use(VueCookies)
app.use(ToastService)
app.component('PrimeProgressSpinner', ProgressSpinner)
app.component('PrimeAccordionTab', AccordionTab)
app.component('PrimeInputNumber', InputNumber)
app.component('PrimeInputSwitch', InputSwitch)
app.component('PrimeInputText', InputText)
app.component('PrimeAccordion', Accordion)
app.component('PrimeDataTable', DataTable)
app.component('PrimeDropdown', Dropdown)
app.component('PrimeCalendar', Calendar)
app.component('PrimeTabPanel', TabPanel)
app.component('PrimeTabView', TabView)
app.component('PrimeDivider', Divider)
app.component('PrimeAvatar', Avatar)
app.component('PrimeColumn', Column)
app.component('PrimeButton', Button)
app.component('PrimeBadge', Badge)
app.component('PrimeToast', Toast)
app.component('PrimeChart', Chart)
app.component('PrimeChip', Chip)
app.component('PrimeCard', Card)
app.component('PrimeTag', Tag)
app.mount('#app')
