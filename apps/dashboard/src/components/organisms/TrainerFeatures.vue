<template>
    <div class="row">
        <ContentForm :title="'Filters'">
            <FeaturesMapPicker :featuresMapsNames="featuresMapsNames" />
        </ContentForm>
    </div>
</template>

<script>
import FeaturesMapPicker from '../molecules/FeaturesMapPicker.vue'
import ContentForm from '../molecules/ContentForm.vue'
import axios from 'axios'

export default {
    name: 'trainer-features',
    components: {
      FeaturesMapPicker,
      ContentForm,
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
          featuresMapsNames: []
      }  
    },
    methods: {
        getApiFeaturesMapsNames(){
            this.featuresMapsNames = []
            axios.get('http://trainer'+this.$store.state.apis_domain+'/features/get/features_maps/names')
                .then(response => {this.featuresMapsNames = response.data})
                .catch(error => {this.featuresMapsNames = error})
        }
    },
    watch: {
       symbol(){
       }  
    },
    mounted(){
        this.getApiFeaturesMapsNames()
    }
}
</script>