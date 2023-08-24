<template>
    <component :is="currentComponent" :app="app" :view="view" :symbol="symbol" :key="symbol" />
</template>

<script>

// scrapper
import ScrapperKlines from '@/views/ScrapperKlines.vue'
import ScrapperTalib from '@/views/ScrapperTalib.vue'
// trainer
import TrainerDatasets from '@/views/TrainerDatasets.vue'
import TrainerModels from '@/views/TrainerModels.vue'
import TrainerDarwin from '@/views/TrainerDarwin.vue'
// trader

export default {
    name: 'content-panel',
    components: {
        ScrapperKlines,
        ScrapperTalib,
        TrainerDatasets,
        TrainerModels,
        TrainerDarwin
    },
    props: ['app','view','symbol','currentComponent'],
}
</script>