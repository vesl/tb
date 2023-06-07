<template>
    <PrimeCard>
        <template #title v-if="selectedDatasetsName">Dataset <span class="text-green-500">{{ selectedDatasetsName }}</span></template>
        <template #title v-else>Select a dataset</template>
        <template #content>
            <div class="flex flex-wrap">
                <div class="flex-auto">
                    <label class="text-sm block mb-2">Type</label>
                    <PrimeDropdown v-model="selectedDatasetsType" :options="datasetsTypes" placeholder="select a dataset type" class="mr-2" />
                </div>
                <div class="flex-auto">
                    <label class="text-sm block mb-2">Name</label>
                    <PrimeDropdown v-model="selectedDatasetsName" :options="datasetsNames" placeholder="select a dataset name" class="mr-2" />
                </div>
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import axios from 'axios'

export default {
    props: ['selectedDataset'],
    data(){
        return {
            datasetsTypes: [],
            datasetsNames: [],
            selectedDatasetsType: this.$cookies.get("selectedDatasetsType") ? this.$cookies.get("selectedDatasetsType") : null,
            selectedDatasetsName: this.$cookies.get("selectedDatasetsName") ? this.$cookies.get("selectedDatasetsName") : null
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
        selectedDatasetsType(type) {
            this.selectedDatasetsName = null
            this.getDatasetsNames(type)
            this.$cookies.set("selectedDatasetsType",type)
        },
        selectedDatasetsName(name) {
            this.$emit('update:selectedDataset', name)
            this.$cookies.set('selectedDatasetsName', name)
        }
    },
    mounted() {
        this.getDatasetsTypes()
        if (this.selectedDatasetsType) this.getDatasetsNames(this.selectedDatasetsType)
    }
}
</script>