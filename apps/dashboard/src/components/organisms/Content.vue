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
import TrainerDatasets from './TrainerDatasets.vue'

export default {
    name: 'content-panel',
    components: {
        Header,
        ScrapperKlines,
        TrainerDatasets
    },
    data(){
      return {
          app: this.$route.params.app,
          view: this.$route.params.view,
          symbol: this.$route.params.symbol,
          currentComponent: this.$stringFunctions.firstLetterUpper(this.$route.params.app)+this.$stringFunctions.firstLetterUpper(this.$route.params.view)
      }  
    },
    watch: {
        $route(to) {
            this.app = to.params.app
            this.view = to.params.view
            this.symbol = to.params.symbol
            this.currentComponent = this.$stringFunctions.firstLetterUpper(this.$route.params.app)+this.$stringFunctions.firstLetterUpper(this.$route.params.view)
        }
    },
}
</script>