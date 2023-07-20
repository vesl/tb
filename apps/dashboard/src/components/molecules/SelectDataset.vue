<template>
    <PrimeCard>
        <template #title v-if="selectedDataset">Dataset <span class="text-success">{{ selectedDataset }}</span></template>
        <template #title v-else>Select a dataset</template>
        <template #content>
            <div class="flex flex-wrap">
                <SelectApi app="trainer" uri="/datasets/get/types" title="Type" v-model:output.sync="type" />
                <SelectApi app="trainer" :uri="'/datasets/get/names/'+type" title="Name" v-model:output.sync="selectedDataset" :key="type" />
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import SelectApi from '@/components/atoms/SelectApi.vue'

export default {
    props: ['dataset'],
    components: {
      SelectApi  
    },
    data(){
        return {
            type: null,
            selectedDataset: null,
        }
    },
    watch: {
        selectedDataset(dataset) {
            this.$emit('update:dataset', dataset)
        }
    }
}
</script>