<template>
    <PrimeCard>
        <template #title v-if="output == 'name' && selectedName">Dataset name <span class="text-success">{{ selectedName }}</span></template>
        <template #title v-else-if="output == 'type' && selectedType">Dataset type <span class="text-success">{{ selectedType }}</span></template>
        <template #title v-else>Select dataset {{ output }}</template>
        <template #content>
            <div class="flex flex-wrap">
                <SelectApi app="trainer" uri="/datasets/get/types" title="Type" v-model:output.sync="selectedType" />
                <SelectApi app="trainer" :uri="'/datasets/get/names/'+selectedType" title="Name" v-model:output.sync="selectedName" :key="selectedType" v-if="output == 'name'" />
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import SelectApi from '@/components/atoms/SelectApi.vue'

export default {
    name: 'select-dataset',
    props: ['datasetType','datasetName','output'],
    components: {
      SelectApi  
    },
    data(){
        return {
            selectedType: null,
            selectedName: null,
        }
    },
    watch: {
        selectedType(type) {
            if (this.output == 'type') this.$emit('update:datasetType', type)
        },
        selectedName(name) {
            if (this.output == 'name') this.$emit('update:datasetName', name)
        }
    }
}
</script>