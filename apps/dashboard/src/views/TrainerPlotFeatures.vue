<template>

    <div class="p-3">

        <PlotForm :plotFunction="getplotsFeaturesApiData" :plotting="plotting" :plotCondition="selectedFeaturesMap == null ? false:true">
            <div class="flex-auto">
                <label class="text-sm block mb-2">Features Maps</label>
                <PrimeDropdown v-if="featuresMaps" v-model="selectedFeaturesMap" :options="featuresMaps.map(featuresMap => featuresMap.name)" placeholder="Select a features maps" class="mr-2" />
            </div>
        </PlotForm>
        
        <p v-for="featureName in featuresNames" :key="featureName">
            <PrimeCard>
                <template #title>
                    <span>{{ featureName }}</span>
                </template>
                <template #content>
                    <LWChart v-if="featuresData && featureName in featuresData" type="line" :data="featuresData[featureName]" />
                    <PrimeProgressSpinner v-else />
                </template>
            </PrimeCard>
        </p>

    </div>

</template>

<script>
import PlotForm from '@/components/molecules/PlotForm.vue'
import LWChart from '@/components/atoms/LWChart.vue'
import axios from 'axios'

export default {
    name: 'trainer-features',
    components:{
      PlotForm,
      LWChart
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
          featuresMaps: null,
          featuresData: null,
          featuresNames: null,
          selectedFeaturesMap: null,
          plotting: false
      }  
    },
    methods: {
        getFeaturesMapsApiData(){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/features/get/maps')
                .then(response => {this.featuresMaps = response.data})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        },
        getplotsFeaturesApiData(start,end){
            let featuresMap = this.featuresMaps.find(featuresMap => featuresMap.name == this.selectedFeaturesMap)
            this.plotting = true
            this.featuresData = {}
            this.featuresNames = Object.keys(featuresMap.features)

            axios.post('http://trainer'+this.$store.state.apis_domain+'/features/plot/'+start+'/'+end+'/'+this.$route.params.symbol+'/historical',featuresMap,{headers:{'Content-Type':'application/json'}})
                .then(response => {
                    this.featuresPlots = {}
                    let JSONData = JSON.parse(response.data)
                    let features = Object.keys(JSONData[0])
                    features.forEach((feature) => {
                        if (feature == 'time') return
                        this.featuresData[feature.split('!')[0]] = JSONData.map( record => { 
                            return {
                                time: record.time,
                                value: record[feature]
                            }
                        })

                    })
                    this.plotting = false
                })
                .catch(error => {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })
                    this.plotting = false
                })
        }  
    },
    watch: {
        symbol(){
            this.featuresData = null
            this.featuresNames = null
        }  
    },
    mounted(){
        this.getFeaturesMapsApiData()
    }
}
</script>