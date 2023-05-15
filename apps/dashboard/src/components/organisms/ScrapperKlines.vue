<template>
    <div class="row">
        <ContentText :title="'First Live Kline'">
            <KlineDetail :kline="firstLiveKline" v-if="Object.keys(firstLiveKline).length > 0" />
            <Loading v-else />
        </ContentText>
        <ContentText :title="'Last Live Kline'">
            <KlineDetail :kline="lastLiveKline" v-if="Object.keys(lastLiveKline).length > 0" />
            <Loading v-else />
        </ContentText>
        <ContentChart :title="'Live Klines'">
            <LWChart :type="'candlestick'" :data="liveKlines" v-if="liveKlines.length > 0 && 'time' in liveKlines[0]" />
            <Loading v-else />
        </ContentChart>
        <ContentText :title="'First Historical Kline'">
            <KlineDetail :kline="firstHistoricalKline" v-if="Object.keys(firstHistoricalKline).length > 0" />
            <Loading v-else />
        </ContentText>
        <ContentText :title="'Last Historical Kline'">
            <KlineDetail :kline="lastHistoricalKline" v-if="Object.keys(lastHistoricalKline).length > 0" />
            <Loading v-else />
        </ContentText>
        <ContentChart :title="'Historical Klines'">
            <LWChart :type="'candlestick'" :data="historicalKlines" v-if="historicalKlines.length > 0 && 'time' in historicalKlines[0]" />
            <Loading v-else />
        </ContentChart>
    </div>
</template>

<script>
import ContentChart from '../molecules/ContentChart.vue'
import ContentText from '../molecules/ContentText.vue'
import KlineDetail from '../atoms/KlineDetail.vue'
import Loading from '../atoms/Loading.vue'
import LWChart from '../atoms/LWChart.vue'
import axios from 'axios'

export default {
    name: 'scrapper-klines',
    components: {
      ContentChart,
      ContentText,
      KlineDetail,
      Loading,
      LWChart
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
          liveKlines: {},
          historicalKlines: {},
          firstLiveKline: {},
          firstHistoricalKline: {},
          lastLiveKline: {},
          lastHistoricalKline: {}
      }  
    },
    methods: {
        getApiData(){
            // reset all props to display loading immediately if symbol changes
            this.liveKlines = {}
            this.historicalKlines = {}
            this.lastLiveKline = {}
            this.lastHistoricalKline = {}
            // get Api data
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/live/'+this.symbol)
                .then(response => {this.liveKlines = JSON.parse(response.data)})
                .catch(error => {this.liveKlines = error})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/historical/'+this.symbol)
                .then(response => {this.historicalKlines = JSON.parse(response.data)})
                .catch(error => {this.historicalKlines = error})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/live/'+this.symbol)
                .then(response => {this.lastLiveKline = JSON.parse(response.data)[0]})
                .catch(error => {this.lastLiveKline = error})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/historical/'+this.symbol)
                .then(response => {this.lastHistoricalKline = JSON.parse(response.data)[0]})
                .catch(error => {this.lastHistoricalKline = error})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/first/live/'+this.symbol)
                .then(response => {this.firstLiveKline = JSON.parse(response.data)[0]})
                .catch(error => {this.firstLiveKline = error})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/first/historical/'+this.symbol)
                .then(response => {this.firstHistoricalKline = JSON.parse(response.data)[0]})
                .catch(error => {this.firstHistoricalKline = error})
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