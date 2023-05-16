<template>
    <ContentText :title="'Features maps'">
        <Collapse v-for="featuresMap in featuresMaps" :key="featuresMap.function_group" :title="featuresMap.function_group">
            <FeaturesMapDetail  :featuresMap="featuresMap" />
        </Collapse>
    </ContentText>
</template>

<script>
import FeaturesMapDetail from '../molecules/FeaturesMapDetail.vue'
import ContentText from '../molecules/ContentText.vue'
import Collapse from '../molecules/Collapse.vue'
import Loading from '../atoms/Loading.vue'
import axios from 'axios'

export default {
    name: 'scrapper-talib',
    components: {
      FeaturesMapDetail,
      ContentText,
      Collapse,
      Loading
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
          featuresMaps : []
      }
    },
    methods: {
        getApiData(){
            this.featuresMaps = []
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/get/features_maps')
                .then(response => {this.featuresMaps = response.data})
                .catch(error => {this.featuresMaps = error})
        }
    },
    mounted(){
        this.getApiData()
    }
}
</script>