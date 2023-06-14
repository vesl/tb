<template>
    <div class="p-2">
        <PrimeDivider />
        <SelectDataset v-model:dataset.sync="dataset" />
        <PrimeDivider />
        <FeaturesMapsTable v-if="dataset" :dataset="dataset" :key="dataset" />
        <PrimeDivider />
        <PlotDatasetFeatures v-if="dataset" :dataset="dataset" :key="dataset" />
    </div>
</template>

<script>
import PlotDatasetFeatures from '@/components/molecules/PlotDatasetFeatures.vue'
import FeaturesMapsTable from '@/components/molecules/FeaturesMapsTable.vue'
import SelectDataset from '@/components/molecules/SelectDataset.vue'

export default {
    name: 'trainer-datasets',
    components: {
        PlotDatasetFeatures,
        FeaturesMapsTable,
        SelectDataset
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
    },
    data() {
        return {
            dataset: this.$cookies.get("selectedDataset") ? this.$cookies.get("selectedDataset") : null,
        }
    }
}
</script>