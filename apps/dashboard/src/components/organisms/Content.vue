<template>
    <div class="row shadow">
        <Header :title="$stringFunctions.firstLetterUpper(app+' '+view)" />
    </div>
    <div class="row p-4">
        <component :is="currentComponent" :app="app" :view="view" :symbol="symbol" />
    </div>
</template>

<script>
import Header from '../molecules/Header.vue'
import ScrapperKlines from './ScrapperKlines.vue'
import ScrapperTalib from './ScrapperTalib.vue'
import TrainerDatasets from './TrainerDatasets.vue'

export default {
    name: 'content-panel',
    components: {
        Header,
        ScrapperKlines,
        ScrapperTalib,
        TrainerDatasets
    },
    data(){
      return {
          app: this.$route.params.app,
          view: this.$route.params.view,
          symbol: this.$route.params.symbol,
          currentComponent: this.computeCurrentComponent()
      }  
    },
    methods: {
      computeCurrentComponent(){
          return this.$stringFunctions.firstLetterUpper(this.$route.params.app)+this.$stringFunctions.firstLetterUpper(this.$route.params.view).replace(/\s+/g, '')
      }  
    },
    watch: {
        $route(to) {
            this.app = to.params.app
            this.view = to.params.view
            this.symbol = to.params.symbol
            this.currentComponent = this.computeCurrentComponent()
        }
    },
}
</script>