<template>
    <PrimeCard>
        <template #title>Features Maps Table</template>
        <template #content>
            <PrimeAccordion v-if="featuresMaps" :multiple="true">
                <PrimeAccordionTab v-for="(featuresMap,index) in featuresMaps" :key="index" :header="featuresMap.name">
                    <PrimeDataTable :value="formatFeatures(featuresMap.features)" stripedRows>
                        <PrimeColumn field="name" header="Name">
                            <template #body="slotProps">
                                <strong>{{ slotProps.data.name }}</strong>
                            </template>
                        </PrimeColumn>
                        <PrimeColumn field="args" header="Args">
                            <template #body="slotProps">
                                <PrimeTag v-for="(value,arg) in slotProps.data.args" :key="arg" severity="warning" class="m-2">
                                    <span class="ml-2 mr-2 font-medium">{{ arg }}</span>
                                    <span class="primary-dark w-2rem h-2rem flex align-items-center justify-content-center">{{ value }}</span>
                                </PrimeTag>
                            </template>
                        </PrimeColumn>
                        <PrimeColumn field="klines_args" header="Klines Args">
                            <template #body="slotProps">
                                <PrimeTag v-for="klines_arg in slotProps.data.klines_args" :key="klines_arg" severity="danger" class="m-2" >
                                    <span class="ml-2 mr-2 font-medium">{{ klines_arg }}</span>
                                </PrimeTag>
                            </template>
                        </PrimeColumn>
                        <PrimeColumn field="lag" header="Lag">
                            <template #body="slotProps">
                                <PrimeBadge :value="'lag' in slotProps.data ? slotProps.data.lag:0" size="large" severity="info" />
                            </template>
                        </PrimeColumn>
                    </PrimeDataTable>
                </PrimeAccordionTab>
            </PrimeAccordion>
        </template>
    </PrimeCard>
</template>

<script>
import axios from "axios"

export default {
    name: 'features-maps-table',
    props: ['datasetName'],
    data() {
      return {
          featuresMaps: null
      }  
    },
    methods: {
        formatFeatures(features){
            return Object.keys(features).map(key => {
                return Object.assign({name:key},features[key])
            })
        },
        getFeaturesMaps(){
            this.featuresMaps = []
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/features_maps/'+this.datasetName)
                .then(response => {this.featuresMaps = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
        },
    },
    mounted(){
        this.getFeaturesMaps()
    }
}
</script>