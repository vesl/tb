<template>

    <div class="p-3">

        <PlotForm :plotFunction="plotFeatures" :plotting="plotting" :plotCondition="selectedFeaturesMap == null ? false:true">
            <div class="flex-auto">
                <label class="text-sm block mb-2">Features Maps</label>
                <PrimeDropdown v-if="featuresMaps" v-model="selectedFeaturesMap" :options="featuresMaps.map(featuresMap => featuresMap.name)" placeholder="Select a features maps" class="mr-2" />
            </div>
        </PlotForm>

    </div>

</template>

<script>
import PlotForm from '@/components/molecules/PlotForm.vue'
import axios from 'axios'

export default {
    name: 'trainer-features',
    components:{
      PlotForm  
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
        plotFeatures(startDate,endDate){
            this.plotting=true
            console.log()
        }  
    },
    watch: {
       symbol(){
       }  
    },
    mounted(){
        this.getFeaturesMapsApiData()
    }
}
</script>