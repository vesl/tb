<template>
    <SelectDataset v-model:dataset.sync="dataset" />
    <PrimeDivider v-if="dataset" />
    <SelectModelType v-if="dataset" v-model:type.sync="type" />
    <PrimeDivider v-if="type" />
    <PrimeCard v-if="type">
        <template #title>Save</template>
        <template #content>
            <PrimeInputSwitch inputId="save" v-model="save" />
        </template>
    </PrimeCard>
    <PrimeDivider v-if="type" />
    <PrimeCard v-if="type">
        <template #title>Configuration</template>
        <template #content>
            <FormObject v-if="parameters_map" submitText="Train" :submitFunction="train" :loading="Boolean(training)" :object="parameters_map" />
        </template>
    </PrimeCard>
    <PrimeDivider v-if="perfs && type" />
    <RandomForestPerfs v-if="perfs && type === 'random_forest'" :perfs="perfs" :name="name" />
</template>

<script>
import RandomForestPerfs from '@/components/atoms/RandomForestPerfs.vue'
import SelectModelType from '@/components/molecules/SelectModelType.vue'
import SelectDataset from '@/components/molecules/SelectDataset.vue'
import FormObject from '@/components/atoms/FormObject.vue'
import axios from "axios"

export default {
    name: 'train-model',
    components: {
      RandomForestPerfs,
      SelectModelType,
      SelectDataset,
      FormObject
    },
    data() {
        return {
            parameters_map: null,
            training: null,
            dataset: null,
            save: false,
            perfs: null,
            name: null,
            type: null,
        }
    },
    watch: {
        type(type){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/models/get/parameters_map/'+type)
                .then(response => {
                    this.parameters_map = response.data
                    this.perfs = null
                })
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
    methods: {
        train(form) {
            this.training = 1
            this.perfs = null
            let modelMap = { save: this.save, dataset_name: this.dataset, parameters_map: form }
            axios.post('http://trainer'+this.$store.state.apis_domain+'/models/train/'+this.type+'/'+this.$route.params.symbol,modelMap,{headers:{'Content-Type':'application/json'}})
                .then((response) => {
                    this.training = 0
                    this.name = response.data.name
                    this.perfs = response.data.perfs
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Model trained in '+this.perfs.training_time})
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