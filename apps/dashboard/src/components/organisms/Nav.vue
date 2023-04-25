<template>
  <div class="row">
    <Title :title="appName" />
  </div>
  <div class="row" v-for="(menu,index) in menus" :key="index" :menu="menu">
    <div class="menu-header shadow-sm">
        <div class="ml-3 p-2">
            <Icon :icon="menu.icon" />
            <span>{{ $stringFunctions.firstLetterUpper(menu.name) }}</span>
        </div>
    </div>
    <div v-for="(child, index) in menu.children" :key="index">
      <div :class="{'selected' : selectedMenu == menu.name && selectedChild == child.name }" class="menu-item p-3 tb-fade" @click="select(menu.name,child.name)">
        <span class="p-2">{{ $stringFunctions.firstLetterUpper(child.name) }}</span>
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
      selectedMenu: 0,
      selectedChild: 0,
      menus: [
        {
          name: 'scrapper',
          icon: 'bi-box-arrow-in-left',
          children: [
            {
              name: 'klines',
            }
          ]
        },
        {
          name: 'plotter',
          icon: 'bi-bar-chart',
          children: [
            {
              name: 'datasets',
            }
          ]
        },
        {
          name: 'trainer',
          icon: 'bi-train-freight-front',
          children: [
            {
              name: 'models',
            },
            {
              name: 'darwin',
            }
          ]
        },
        {
          name: 'trader',
          icon: 'bi-currency-dollar',
          children: [
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
    select(menu,child) {
      this.selectedMenu = menu
      this.selectedChild = child
      this.$router.push('/'+menu+'/'+child)
    }
  }
}
</script>

<style scoped>
.menu-header {
  color: var(--middle-light);
  font-size: 0.8em;
}
.menu-item:hover {
  background-color: var(--middle-dark);
  border-left: 8px solid var(--flash);
}
.selected {
  background-color: var(--middle-dark);
  border-left: 8px solid green;
}
.selected:hover {
  background-color: var(--middle-dark);
  border-left: 8px solid green;
}
</style>