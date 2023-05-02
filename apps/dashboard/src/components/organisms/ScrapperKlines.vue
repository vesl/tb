<template>
    <div class="row">
        <ContentText :title="'Last Live Kline'">
            <KlineDetail :kline="lastLiveKline" />
        </ContentText>
        <ContentText :title="'Last Historical Kline'">
            <KlineDetail :kline="lastHistoricalKline" />
        </ContentText>
        <ContentChart :title="'Live Klines'">
            a
        </ContentChart>
        <ContentChart :title="'Historical Klines'">
            a
        </ContentChart>
    </div>
</template>

<script>
import ContentChart from '../molecules/ContentChart.vue'
import ContentText from '../molecules/ContentText.vue'
import KlineDetail from '../molecules/KlineDetail.vue'
import axios from 'axios';

export default {
    name: 'scrapper-klines',
    components: {
      ContentChart,
      ContentText,
      KlineDetail
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