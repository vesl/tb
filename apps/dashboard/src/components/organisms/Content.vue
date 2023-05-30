<template>
    <component :is="currentComponent" :app="app" :view="view" :symbol="symbol" />
</template>

<script>

// scrapper
import ScrapperKlines from '@/views/ScrapperKlines.vue'
import ScrapperTalib from '@/views/ScrapperTalib.vue'
// trainer
import TrainerPlotFeatures from '@/views/TrainerPlotFeatures.vue'
import TrainerDatasets from '@/views/TrainerDatasets.vue'
// trader

export default {
    name: 'content-panel',
    components: {
        ScrapperKlines,
        ScrapperTalib,
        TrainerPlotFeatures,
        TrainerDatasets
    },
    props: {
      app: {
          type: String,
          required: true
      },
      view: {
          type: String,
          required: true
      },
      symbol: {
          type: String,
          required: true
      },
      currentComponent: {
          type: String,
          required: true
      }
    }
}
</script>