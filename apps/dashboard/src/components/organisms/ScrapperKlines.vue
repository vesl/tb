<template>
    <div class="row">
        <ContentInfo :class="'col-5'" :title="'Last Live Kline'">
            {{ lastLiveKline }}
        </ContentInfo>
        <ContentInfo :class="'col-5'" :title="'Last Live Kline'">
            {{ lastHistoricalKline }}
        </ContentInfo>
    </div>
</template>

<script>
import ContentInfo from '../molecules/ContentInfo.vue'
import axios from 'axios';

export default {
    name: 'scrapper-klines',
    components: {
      ContentInfo
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
          lastLiveKline: null,
          lastHistoricalKline: null
      }  
    },
    mounted(){
        axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/live/'+this.symbol)
            .then(response => {this.lastLiveKline = JSON.parse(response.data)})
            .catch(error => {this.lastLiveKline = error;});
        axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/historical/'+this.symbol)
            .then(response => {this.lastHistoricalKline = JSON.parse(response.data)})
            .catch(error => {this.lastHistoricalKline = error;});
    }
}
</script>