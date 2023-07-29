<template>
    <div class="p-2">
        <SelectDataset v-model:datasetName.sync="datasetName" output="name" />
        <PrimeDivider />
        <FeaturesMapsTable v-if="datasetName" :dataset="datasetName" :key="datasetName" />
        <PrimeDivider />
        <PlotDatasetFeatures v-if="datasetName" :dataset="datasetName" :key="datasetName" />
        <PrimeDivider />
        <PlotDatasetEvents v-if="datasetName" :dataset="datasetName" :key="datasetName" />
        <PrimeDivider />
        <PlotDatasetLabels v-if="datasetName" :dataset="datasetName" :key="datasetName" />
    </div>
</template>

<script>
import PlotDatasetFeatures from '@/components/molecules/PlotDatasetFeatures.vue'
import PlotDatasetLabels from '@/components/molecules/PlotDatasetLabels.vue'
import PlotDatasetEvents from '@/components/molecules/PlotDatasetEvents.vue'
import FeaturesMapsTable from '@/components/atoms/FeaturesMapsTable.vue'
import SelectDataset from '@/components/molecules/SelectDataset.vue'

export default {
    name: 'trainer-datasets',
    components: {
        PlotDatasetFeatures,
        PlotDatasetLabels,
        PlotDatasetEvents,
        FeaturesMapsTable,
        SelectDataset
    },
    props: ['app','view','symbol'],
    data() {
        return {
            datasetName: null,
        }
    }
}
</script>