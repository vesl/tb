<template>
  <div class="grid min-h-screen">
      <Header :app="app" :view="view" :symbol="symbol" />
      <!-- left -->
      <div class="primary col-2 p-0">
        <Nav />
      </div>
      <!-- right -->
      <div class="secondary col-10 p-0">
        <router-view :app="app" :view="view" :symbol="symbol" :currentComponent="currentComponent" />
      </div>
  </div>
</template>

<script>
import Header from './components/organisms/Header.vue'
import Nav from './components/organisms/Nav.vue'

export default {
  name: 'App',
  components: {
    Header,
    Nav
  },
  data(){
    return {
      app: null,
      view: null,
      symbol: null,
      currentComponent: null
    }
  },
  watch: {
    $route(to) {
      this.app = to.params.app
      this.view = to.params.view
      this.symbol = to.params.symbol
      this.currentComponent = this.$stringFunctions.firstLetterUpper(this.$route.params.app)+this.$stringFunctions.firstLetterUpper(this.$route.params.view).replace(/\s+/g, '')
    }
  }
}
</script>