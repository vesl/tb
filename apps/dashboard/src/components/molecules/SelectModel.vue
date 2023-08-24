<template>
    <PrimeCard>
        <template #title v-if="output == 'name' && selectedName">Model name <span class="text-success">{{ selectedName }}</span></template>
        <template #title v-else-if="output == 'type' && selectedType">Model type <span class="text-success">{{ selectedType }}</span></template>
        <template #title v-else>Select model {{ output }}</template>
        <template #content>
            <div class="flex flex-wrap">
                <SelectApi app="trainer" uri="/models/get/types" title="Type" v-model:output.sync="selectedType" />
                <SelectApi app="trainer" :uri="'/models/get/names/'+selectedModelType" title="Name" v-model:output.sync="selectedName" :key="selectedType" v-if="output == 'name'" />
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import SelectApi from '@/components/atoms/SelectApi.vue'

export default {
    name: 'select-model-type',
    props: ['modelType','modelName','output'],
    components: {
        SelectApi
    },
    data(){
        return {
            selectedType: null,
            selectedName: null
        }
    },
    watch: {
        selectedType(type) {
            if (this.output == 'type') this.$emit('update:modelType', type)
        },
        selectedName(name) {
            if (this.output == 'name') this.$emit('update:modelName', name)
        }
    }
}
</script>