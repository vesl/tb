<template>
    <LWChart v-if="klines" type="candlestick" :data="klines" :markers="markers" />
    <PrimeProgressSpinner v-else />
</template>

<script>
import LWChart from '@/components/atoms/LWChart.vue'
import axios from "axios"

export default {
    name: 'plot-klines',
    props: ['period','markers','symbol'],
    components: {
        LWChart
    },
    data(){
        return {
            klines: null
        }
    },
    methods: {
        getKlines(){
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/'+this.period+'/'+this.symbol)
                .then(response => {this.klines = JSON.parse(response.data)})
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        }
    },
    mounted(){
        this.getKlines()
    }
}
</script>