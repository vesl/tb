<template>
    <PrimeTabView>
        <PrimeTabPanel header="Stats">
            <ModelsTable :symbol="symbol" :key="symbol" />
        </PrimeTabPanel>
        <PrimeTabPanel header="Train">
            <TrainModel />
        </PrimeTabPanel>
    </PrimeTabView>
</template>

<script>
import TrainModel from '@/components/molecules/TrainModel.vue'
import ModelsTable from '@/components/atoms/ModelsTable.vue'

export default {
    name: 'trainer-datasets',
    components: {
        ModelsTable,
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
    }
}
</script>