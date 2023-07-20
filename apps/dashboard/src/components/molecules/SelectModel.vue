<template>
    <PrimeCard>
        <template #title v-if="selectedModel">Model <span class="text-success">{{ selectedModel }}</span></template>
        <template #title v-else>Select a model</template>
        <template #content>
            <div class="flex flex-wrap">
                <SelectApi app="trainer" uri="/models/get/types" title="Type" v-model:output.sync="type" />
                <SelectApi app="trainer" :uri="'/models/get/names/'+type" title="Name" v-model:output.sync="selectedModel" :key="type" />
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import SelectApi from '@/components/atoms/SelectApi.vue'
import axios from 'axios'

export default {
    props: ['model'],
    components: {
        SelectApi,
    },
    data(){
        return {
            type: null,
            selectedModel: null,
        } 
    },
    watch: {
        selectedModel(model) {
            this.$emit('update:model', model)
        }
    },
}
</script>