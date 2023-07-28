<template>
    <div class="flex-auto">
        <SelectApi app="trainer" :uri="'/datasets/get/features_maps_names/'+this.dataset" title="Features Maps" v-model:output.sync="selectedFeaturesMap" />
    </div>
</template>

<script>
import SelectApi from '@/components/atoms/SelectApi.vue'
import axios from "axios"

export default {
    props: ['featuresMap','dataset'],
    components: {
      SelectApi  
    },
    data(){
      return {
          selectedFeaturesMap: null,
      }  
    },
    watch: {
        selectedFeaturesMap(featuresMap) {
            axios.get('http://trainer'+this.$store.state.apis_domain+'/features/get/map/'+featuresMap)
                .then(response => {this.$emit('update:featuresMap', response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
}
</script>