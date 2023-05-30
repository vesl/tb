<template>

    <div class="p-3">
        
        <PrimeCard>
            <template #title>Scrap talib features maps</template>
            <template #content>
                <PrimeButton type="button" label="Scrap" icon="pi pi-sync" :loading="scrapping" @click="scrapFeaturesMaps" />
            </template>
        </PrimeCard>

        <PrimeDivider />

        <PrimeCard>
            <template #title>Features maps</template>
            <template #content>
                <PrimeAccordion v-if="featuresMaps" :multiple="true">
                    <PrimeAccordionTab v-for="(featuresMap,index) in featuresMaps" :key="index" :header="featuresMap.name">
                        <FeaturesDetail :features="featuresMap.features" />
                    </PrimeAccordionTab>
                </PrimeAccordion>
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>

    </div>

</template>

<script>
import FeaturesDetail from '@/components/molecules/FeaturesDetail.vue'
import axios from 'axios'

export default {
    name: 'scrapper-talib',
    components : {
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
    data (){
      return {
          featuresMaps : null,
          scrapping : false
      }
    },
    methods: {
        getTalibFeaturesMapsApiData(){
            this.featuresMaps = []
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/get/features_maps')
                .then(response => {this.featuresMaps = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
        },
        scrapFeaturesMaps(){
            this.scrapping = true
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/scrap/features_maps')
                .then(response => {
                    this.getApiData()
                    this.scrapping = false
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: response.data, life: 3000 })
                })
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
        }
    },
    mounted(){
        this.getTalibFeaturesMapsApiData()
    }
}
</script>