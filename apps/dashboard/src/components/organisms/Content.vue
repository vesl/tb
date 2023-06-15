<template>
    <component :is="currentComponent" :app="app" :view="view" :symbol="symbol" :key="symbol" />
</template>

<script>

// scrapper
import ScrapperKlines from '@/views/ScrapperKlines.vue'
import ScrapperTalib from '@/views/ScrapperTalib.vue'
// trainer
import TrainerDatasets from '@/views/TrainerDatasets.vue'
// trader

export default {
    name: 'content-panel',
    components: {
        ScrapperKlines,
        ScrapperTalib,
        TrainerDatasets
    },
    props: ['app','view','symbol','currentComponent'],
}
</script>