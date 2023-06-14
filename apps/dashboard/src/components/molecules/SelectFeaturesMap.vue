<template>
    <div class="flex-auto">
        <label class="text-sm block mb-2">Features Maps</label>
        <PrimeDropdown v-if="featuresMaps" v-model="selectedFeaturesMap" :options="featuresMaps" placeholder="Select a features map" class="mr-2" />
    </div>
</template>

<script>
import axios from "axios"

export default {
    props: ['featuresMap','dataset'],
    data(){
      return {
          selectedFeaturesMap: null,
          featuresMaps: null
      }  
    },
    watch: {
        selectedFeaturesMap(featuresMap) {
            axios.get('http://trainer'+this.$store.state.apis_domain+'/features/get/map/'+featuresMap)
                .then(response => {
                    this.$emit('update:featuresMap', response.data)
                })
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
    methods: {
        getFeaturesMaps(){
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/features_maps/'+this.dataset)
                .then(response => {this.featuresMaps = response.data.map(featuresMap => featuresMap.name)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
    mounted(){
        this.getFeaturesMaps()
    }
}
</script>