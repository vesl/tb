<template>
    <div class="p-2">
        <PrimeTabView>
            <PrimeTabPanel header="Stats">
                <SelectModel v-model:model.sync="model" />
            </PrimeTabPanel>
            <PrimeTabPanel header="Train">
                <SelectDataset v-model:dataset.sync="dataset" />
                <PrimeDivider />
                <TrainModel v-if="dataset" :dataset="dataset" />
            </PrimeTabPanel>
        </PrimeTabView>
    </div>
</template>

<script>
import SelectDataset from '@/components/molecules/SelectDataset.vue'
import SelectModel from '@/components/molecules/SelectModel.vue'
import TrainModel from '@/components/atoms/TrainModel.vue'

export default {
    name: 'trainer-datasets',
    components: {
        SelectDataset,
        SelectModel,
        TrainModel
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
            dataset: null,
            model: null,
        }
    }
}
</script>