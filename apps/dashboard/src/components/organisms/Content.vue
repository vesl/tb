<template>
    <div class="row shadow">
        <Header :title="$stringFunctions.firstLetterUpper(app) +' '+$stringFunctions.firstLetterUpper(view)" />
    </div>
    <div class="row p-4">
        <component :is="currentComponent" :app="app" :view="view" :symbol="symbol" />
    </div>
</template>

<script>
import Header from '../molecules/Header.vue'
import ScrapperKlines from './ScrapperKlines.vue'

export default {
    name: 'content-panel',
    components: {
        Header,
        ScrapperKlines
    },
    data(){
      return {
          app: this.$route.params.app,
          view: this.$route.params.view,
          symbol: this.$route.params.symbol
      }  
    },
    computed: {
        currentComponent(){
            return this.$stringFunctions.firstLetterUpper(this.app)+this.$stringFunctions.firstLetterUpper(this.view)
        }
    },
    watch: {
        $route(to) {
            this.symbol = to.params.symbol
        }
    }
}
</script>