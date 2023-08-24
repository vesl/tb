<template>
    <SelectDataset v-model:datasetName.sync="datasetName" output="name" />
    <PrimeDivider v-if="datasetName" />
    <SelectModel v-if="datasetName" v-model:modelType.sync="modelType" output="type" />
    <PrimeDivider v-if="modelType" />
    <PrimeCard v-if="modelType">
        <template #title>Save</template>
        <template #content>
            <PrimeInputSwitch inputId="modelSave" v-model="modelSave" />
        </template>
    </PrimeCard>
    <PrimeDivider v-if="modelType" />
    <PrimeCard v-if="modelType">
        <template #title>Configuration</template>
        <template #content>
            <FormObject v-if="parametersMap" submitText="Train" :submitFunction="train" :loading="Boolean(training)" :object="parametersMap" />
        </template>
    </PrimeCard>
    <PrimeDivider v-if="modelPerfs && modelType" />
    <RandomForestPerfs v-if="modelPerfs && modelType === 'random_forest'" :perfs="modelPerfs" :name="modelName" />
</template>

<script>
import RandomForestPerfs from '@/components/atoms/RandomForestPerfs.vue'
import SelectDataset from '@/components/molecules/SelectDataset.vue'
import SelectModel from '@/components/molecules/SelectModel.vue'
import FormObject from '@/components/atoms/FormObject.vue'
import axios from "axios"

export default {
    name: 'train-model',
    components: {
        RandomForestPerfs,
        SelectDataset,
        SelectModel,
        FormObject
    },
    data() {
        return {
            parametersMap: null,
            datasetName: null,
            modelSave: false,
            modelPerfs: null,
            modelName: null,
            modelType: null,
            training: null,
        }
    },
    watch: {
        modelType(type){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/models/get/parameters_map/'+type)
                .then(response => {
                    this.parametersMap = response.data
                    this.modelPerfs = null
                })
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
    methods: {
        train(form) {
            this.training = 1
            this.modelPerfs = null
            let modelMap = { save: this.modelSave, dataset_name: this.datasetName, parameters_map: form }
            axios.post('http://trainer'+this.$store.state.apis_domain+'/models/train/'+this.modelType+'/'+this.$route.params.symbol,modelMap,{headers:{'Content-Type':'application/json'}})
                .then((response) => {
                    this.training = 0
                    this.modelName = response.data.name
                    this.modelPerfs = response.data.perfs
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Model trained in '+this.modelPerfs.training_time})
                })
                .catch(error => {
                    this.training = 0
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })
                })
        }
    },
    mounted(){
        axios.get('http://trainer'+this.$store.state.apis_domain+'/models/train/status')
            .then(response => { this.training = response.data})
            .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
    }
}
</script>