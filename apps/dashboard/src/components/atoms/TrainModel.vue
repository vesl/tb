<template>
    <PrimeCard>
        <template #title>Train model</template>
        <template #content>
            <SelectApi app="trainer" uri="/models/get/types" title="Type" v-model:output.sync="type" />
            <CreateModelConfig :type="type" />
        </template>
    </PrimeCard>
</template>

<script>
import CreateModelConfig from '@/components/atoms/CreateModelConfig.vue'
import SelectApi from '@/components/atoms/SelectApi.vue'

export default {
    name: 'train-model',
    props: ['dataset'],
    components: {
      CreateModelConfig,
      SelectApi  
    },
    data() {
        return {
            type: null,
        }
    }
}
</script>