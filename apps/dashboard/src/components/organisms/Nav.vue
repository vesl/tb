<template>
  <div class="row shadow">
    <Title :title="appName" />
  </div>
  <div class="row" v-for="(app,index) in apps" :key="index">
    <div class="nav-header shadow-sm">
        <div class="ml-3 p-2">
            <Icon :icon="app.icon" />
            <span>{{ $stringFunctions.firstLetterUpper(app.name) }}</span>
        </div>
    </div>
    <div v-for="(view, index) in app.views" :key="index">
      <div :class="{'nav-item-selected' : selectedApp == app.name && selectedView == view.name }" class="nav-item p-3 tb-fade" @click="select(app.name,view.name)">
        <span>{{ $stringFunctions.firstLetterUpper(view.name) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import Title from '../atoms/Title.vue'
import Icon from '../atoms/Icon.vue'

export default {
  name: 'nav-panel',
  components: {
    Title,
    Icon
  },
  props: {
    appName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      apps: [
        {
          name: 'scrapper',
          icon: 'bi-box-arrow-in-left',
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
          icon: 'bi-train-freight-front',
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
          icon: 'bi-currency-dollar',
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
  },
  methods: {
    select(app,view) {
      this.$router.push('/'+app+'/'+view+'/'+(this.$route.params.symbol ? this.$route.params.symbol:this.$store.state.symbols[0]))
    }
  },
  computed: {
    selectedApp(){
      return 'app' in this.$route.params ? this.$route.params.app:0
    },
    selectedView(){
      return 'view' in this.$route.params ? this.$route.params.view:0
    }
  }
}
</script>

<style scoped>
.nav-header {
  color: var(--middle-light);
  font-size: 0.8em;
}
.nav-item:hover {
  background-color: var(--middle-dark);
  border-left: 8px solid var(--flash);
}
.nav-item-selected {
  background-color: var(--middle-dark);
  border-left: 8px solid green;
}
.nav-item-selected:hover {
  background-color: var(--middle-dark);
  border-left: 8px solid green;
}
</style>