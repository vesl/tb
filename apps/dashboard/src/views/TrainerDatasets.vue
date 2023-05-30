<template>
    <p v-for="dataset in datasetsMaps" :key="dataset" class="p-2">
        <PrimeCard>
            <template #title>
                {{ $stringFunctions.firstLetterUpper(dataset.name) }}
            </template>
            <template #content>
                <PrimeAccordion :multiple="true">
                    <PrimeAccordionTab v-for="featuresMapName in dataset.features_maps" :key="featuresMapName" :header="featuresMapName">
                        <FeaturesDetail :features="featuresMaps.find( featureMap => featureMap.name == featuresMapName).features" />
                    </PrimeAccordionTab>
                </PrimeAccordion>
            </template>
        
        </PrimeCard>
    </p>
</template>

<script>
import FeaturesDetail from '@/components/molecules/FeaturesDetail.vue'
import axios from 'axios'

export default {
    name: 'trainer-datasets',
    components: {
        FeaturesDetail
    },
    props: {
        app: {
            type: String,
            required: true
        },
        view: {
            type: String,
            required: true
        },
        symbol: {
            type: String,
            required: true
        }
    },
    data(){
        return {
            datasetsMaps: null,
            featuresMaps: null
        }
    },
    methods: {
        getDatasetsMapsApiData(){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/maps')
                .then(response => {this.datasetsMaps = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        },
        getFeaturesMapsApiData(){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/features/get/maps')
                .then(response => {this.featuresMaps = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        },
    },
    mounted(){
        this.getDatasetsMapsApiData()
        this.getFeaturesMapsApiData()
    }
}
</script>