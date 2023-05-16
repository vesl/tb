<template>
    <ContentAction :title="'Scrap talib features maps'">
        <Loading v-if="scrapping" :color="'dark'" />
        <ButtonAction v-else :title="'Scrap'" :action="scrap" />
    </ContentAction>
    <ContentText :title="'Features maps'">
        <Collapse v-for="featuresMap in featuresMaps" :key="featuresMap.function_group" :title="featuresMap.function_group">
            <FeaturesMapDetail  :featuresMap="featuresMap" />
        </Collapse>
    </ContentText>
</template>

<script>
import FeaturesMapDetail from '../molecules/FeaturesMapDetail.vue'
import ContentAction from '../molecules/ContentAction.vue'
import ButtonAction from '../molecules/ButtonAction.vue'
import ContentText from '../molecules/ContentText.vue'
import Collapse from '../molecules/Collapse.vue'
import Loading from '../atoms/Loading.vue'
import axios from 'axios'

export default {
    name: 'scrapper-talib',
    components: {
      FeaturesMapDetail,
      ContentAction,
      ButtonAction,
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
          featuresMaps : [],
          scrapping : false
      }
    },
    methods: {
        getApiData(){
            this.featuresMaps = []
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/get/features_maps')
                .then(response => {this.featuresMaps = response.data})
                .catch(error => {this.featuresMaps = error})
        },
        scrap(){
            this.scrapping = true
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/scrap')
                .then(response => {
                    this.getApiData()
                    this.scrapping = false
                })
                .catch(error => {})
        }
    },
    mounted(){
        this.getApiData()
    }
}
</script>