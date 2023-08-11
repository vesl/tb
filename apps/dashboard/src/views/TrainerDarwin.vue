<template>
    <PrimeTabView>
        <PrimeTabPanel header="Stats">
        </PrimeTabPanel>
        <PrimeTabPanel header="Evolve">
            <SelectDataset v-model:datasetType.sync="datasetType" output="type" />
            <PrimeDivider v-if="datasetType" />
            <SelectModel v-if="datasetType" v-model:modelType.sync="modelType" output="type" />
            <PrimeDivider v-if="modelType" />
            <FormObject v-if="parametersMap" submitText="Evolve" :submitFunction="evolve" :loading="Boolean(evolving)" :object="parametersMap" />
        </PrimeTabPanel>
    </PrimeTabView>
</template>

<script>
import SelectDataset from "@/components/molecules/SelectDataset.vue"
import SelectModel from "@/components/molecules/SelectModel.vue"
import FormObject from "@/components/atoms/FormObject.vue"
import axios from "axios"

export default {
    name: 'trainer-darwin',
    components: {
        SelectDataset,
        SelectModel,
        FormObject
    },
    props: ['app','view','symbol'],
    data() {
        return {
            parametersMap: null,
            datasetType: null,
            modelType: null,
            evolving: null,
        }
    },
    watch: {
        modelType(type){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/darwin/get/parameters_map')
                .then(response => {this.parametersMap = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
    methods: {
        evolve(form){
            this.evolving = 1
            let darwinMap = { dataset_type: this.datasetType, model_type: this.modelType, parameters_map: form }
            axios.post('http://trainer'+this.$store.state.apis_domain+'/darwin/run/'+this.$route.params.symbol,darwinMap,{headers:{'Content-Type':'application/json'}})
                .then((response) => {
                    this.evolving = 0
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Darwin finished' })
                })
                .catch(error => {
                    this.evolving = 0
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })
                })
        }
    },
    mounted(){
        axios.get('http://trainer'+this.$store.state.apis_domain+'/models/train/status')
            .then(response => { this.evolving = response.data})
            .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
    }
}
</script>