<template>
    <PrimeCard>
        <template #title v-if="selectedModelType">Model type <span class="text-success">{{ selectedModelType }}</span></template>
        <template #title v-else>Select model type</template>
        <template #content>
            <SelectApi app="trainer" uri="/models/get/types" title="Type" v-model:output.sync="selectedModelType" />
        </template>
    </PrimeCard>
</template>

<script>
import SelectApi from '@/components/atoms/SelectApi.vue'

export default {
    name: 'select-model-type',
    props: ['type'],
    components: {
        SelectApi
    },
    data(){
        return {
            selectedModelType: null
        }
    },
    watch: {
        selectedModelType(type) {
            this.$emit('update:type', type)
        }
    }
}
</script>