<template>
    <ContentAction :title="'Scrap talib features maps'">
        <Loading v-if="scrapping" :color="'dark'" />
        <ButtonAction v-else :title="'Scrap'" :action="scrapFeaturesMaps" />
    </ContentAction>
    <ContentText :title="'Features maps'">
        <Collapse v-for="featuresMap in featuresMaps" :key="featuresMap.name" :title="featuresMap.name">
            <FeaturesMapDetail  :featuresMap="featuresMap" />
        </Collapse>
    </ContentText>
</template>

<script>
import FeaturesMapDetail from '@/components/molecules/FeaturesMapDetail.vue'
import ContentAction from '@/components/molecules/ContentAction.vue'
import ButtonAction from '@/components/molecules/ButtonAction.vue'
import ContentText from '@/components/molecules/ContentText.vue'
import Collapse from '@/components/molecules/Collapse.vue'
import axios from 'axios'

export default {
    name: 'scrapper-talib',
    components: {
      FeaturesMapDetail,
      ContentAction,
      ButtonAction,
      ContentText,
      Collapse,
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
        scrapFeaturesMaps(){
            this.scrapping = true
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/scrap/features_maps')
                .then(response => {
                    this.getApiData()
                    if (response) this.scrapping = false
                })
                .catch(error => {if(error) this.scrapping = false})
        }
    },
    mounted(){
        this.getApiData()
    }
}
</script>