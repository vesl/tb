<template>
    <div class="row">
        <ContentInfo :class="'col-5'" :title="'Last Live Kline'">
            <KlineInfo :kline="lastLiveKline" />
        </ContentInfo>
        <ContentInfo :class="'col-5'" :title="'Last Historical Kline'">
            <KlineInfo :kline="lastHistoricalKline" />
        </ContentInfo>
    </div>
</template>

<script>
import ContentInfo from '../molecules/ContentInfo.vue'
import KlineInfo from '../molecules/KlineInfo.vue'
import axios from 'axios';

export default {
    name: 'scrapper-klines',
    components: {
      ContentInfo,
      KlineInfo
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
          lastLiveKline: {},
          lastHistoricalKline: {}
      }  
    },
    methods: {
        getApiData(){
            // reset all props to display loading immediately if symbol changes
            this.lastLiveKline = {}
            this.lastHistoricalKline = {}
            // get Api data
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/live/'+this.symbol)
                .then(response => {this.lastLiveKline = JSON.parse(response.data)[0]})
                .catch(error => {this.lastLiveKline = error;});
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/historical/'+this.symbol)
                .then(response => {this.lastHistoricalKline = JSON.parse(response.data)[0]})
                .catch(error => {this.lastHistoricalKline = error;});
        }
    },
    watch: {
       symbol(){
           this.getApiData()
       }  
    },
    mounted(){
        this.getApiData()
    }
}
</script>