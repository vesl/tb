<template>
    
    <PrimeToast />

    <div class="p-3">

        <PrimeCard>
            <template #title>First Live Kline</template>
            <template #content>
                <KlinesDetail v-if="firstLiveKline" :klines="firstLiveKline" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>
        
        <PrimeDivider />
        
        <PrimeCard>
            <template #title>Last Live Kline</template>
            <template #content>
                <KlinesDetail v-if="lastLiveKline" :klines="lastLiveKline" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>
        
        <PrimeDivider />
        
        <PrimeCard>
            <template #title>Live Klines</template>
            <template #content>
                <LWChart v-if="liveKlines" :type="'candlestick'" :data="liveKlines" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>
        
        <PrimeDivider />
        
        <PrimeCard>
            <template #title>First Historical Kline</template>
            <template #content>
                <KlinesDetail v-if="firstHistoricalKline" :klines="firstHistoricalKline" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>

        <PrimeDivider />

        <PrimeCard>
            <template #title>Last Historical Kline</template>
            <template #content>
                <KlinesDetail v-if="lastHistoricalKline" :klines="lastHistoricalKline" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>
        
        <PrimeDivider />
        
        <PrimeCard>
            <template #title>Historical Klines</template>
            <template #content>
                <LWChart v-if="historicalKlines" :type="'candlestick'" :data="historicalKlines" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>

    </div>

</template>

<script>
import KlinesDetail from '@/components/molecules/KlinesDetail.vue'
import LWChart from '@/components/atoms/LWChart.vue'
import axios from 'axios'

export default {
    name: 'scrapper-klines',
    components: {
      KlinesDetail,
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
          liveKlines: null,
          historicalKlines: null,
          firstLiveKline: null,
          firstHistoricalKline: null,
          lastLiveKline: null,
          lastHistoricalKline: null,
      }  
    },
    methods: {
        getApiData(){
            this.liveKlines = null
            this.historicalKlines = null
            this.firstLiveKline = null
            this.firstHistoricalKline = null
            this.lastLiveKline = null
            this.lastHistoricalKline = null
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/live/'+this.symbol)
                .then(response => {this.liveKlines = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/historical/'+this.symbol)
                .then(response => {this.historicalKlines = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/live/'+this.symbol)
                .then(response => {this.lastLiveKline = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/historical/'+this.symbol)
                .then(response => {this.lastHistoricalKline = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/first/live/'+this.symbol)
                .then(response => {this.firstLiveKline = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/first/historical/'+this.symbol)
                .then(response => {this.firstHistoricalKline = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
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