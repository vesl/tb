<template>
    <PrimeCard>
        <template #title v-if="selectedDataset">Dataset <span class="text-success">{{ selectedDataset }}</span></template>
        <template #title v-else>Select a dataset</template>
        <template #content>
            <div class="flex flex-wrap">
                <div class="flex-auto">
                    <label class="text-sm block mb-2">Type</label>
                    <PrimeDropdown v-model="selectedDatasetType" :options="datasetsTypes" placeholder="select a dataset type" class="mr-2" />
                </div>
                <div class="flex-auto">
                    <label class="text-sm block mb-2">Name</label>
                    <PrimeDropdown v-model="selectedDataset" :options="datasetsNames" placeholder="select a dataset name" class="mr-2" filter />
                </div>
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import axios from 'axios'

export default {
    props: ['dataset'],
    data(){
        return {
            selectedDatasetType: this.$cookies.get("selectedDatasetType") ? this.$cookies.get("selectedDatasetType") : null,
            selectedDataset: this.dataset,
            datasetsTypes: [],
            datasetsNames: [],
        }
    },
    methods: {
        getDatasetsTypes(){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/types')
                .then(response => {this.datasetsTypes = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        },
        getDatasetsNames(type){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/names/'+type)
                .then(response => {this.datasetsNames = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        },
    },
    watch: {
        selectedDatasetType(type) {
            this.selectedDatasetsName = null
            this.getDatasetsNames(type)
            this.$cookies.set("selectedDatasetType",type)
        },
        selectedDataset(dataset) {
            this.$emit('update:dataset', dataset)
            this.$cookies.set('selectedDataset', dataset)
        }
    },
    mounted() {
        this.getDatasetsTypes()
        if (this.selectedDatasetType) this.getDatasetsNames(this.selectedDatasetType)
    }
}
</script>