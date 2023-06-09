<template>
    <div class="p-2">
        <SelectDataset v-model:selectedDataset.sync="selectedDataset" />
        <FeaturesMapsTable v-if="selectedDataset" :datasetName="selectedDataset" />
    </div>
</template>

<script>
import FeaturesMapsTable from '@/components/molecules/FeaturesMapsTable.vue'
import SelectDataset from '@/components/molecules/SelectDataset.vue'

export default {
    name: 'trainer-datasets',
    components: {
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
            selectedDataset: null,
        }
    }
}
</script>