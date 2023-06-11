<template>

    <div class="p-3">

        <KlinesTable v-for="period in periods" :key="period" :period="period" :symbol="symbol" />
        
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
            <template #title>Historical Klines</template>
            <template #content>
                <LWChart v-if="historicalKlines" :type="'candlestick'" :data="historicalKlines" />
                <PrimeProgressSpinner v-else />
            </template>
        </PrimeCard>

    </div>

</template>

<script>
import KlinesTable from '@/components/molecules/KlinesTable.vue'
import LWChart from '@/components/atoms/LWChart.vue'
import axios from 'axios'

export default {
    name: 'scrapper-klines',
    components: {
      KlinesTable,
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
          periods: ['live','historical']
      }  
    },
    methods: {
        getApiData(){
            this.liveKlines = null
            this.historicalKlines = null
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/live/'+this.symbol)
                .then(response => {this.liveKlines = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/historical/'+this.symbol)
                .then(response => {this.historicalKlines = JSON.parse(response.data)})
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