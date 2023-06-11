<template>
    <PrimeCard>
        <template #title>Klines Table - {{period}}</template>
        <template #content>
            <PrimeDataTable v-if="firstLastKlines.length" :value="firstLastKlines" showGridlines>
                <PrimeColumn v-for="column in columns" :key="column" :field="column" :header="column" />
            </PrimeDataTable>
        </template>
    </PrimeCard>
    <PrimeDivider />
</template>

<script>
import axios from "axios"

export default {
    name: 'klines-table',
    props: ['period','symbol'],
    data(){
        return {
            firstLastKlines: [],
            klinesCount: 0,
            columns: [],
        }
    },
    methods: {
        formatDate(klines){
            return klines.map( kline => {
                Object.keys(kline).forEach((key)=>{
                    if(key == 'open_time' || key == 'close_time') kline[key] = new Date(kline[key]).toUTCString()
                })
                return kline
            })
        },
        getFirstLastKlines(){
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/first/'+this.period+'/'+this.symbol)
                .then(response => {
                    
                    let firstKline = this.formatDate(JSON.parse(response.data))
                    this.firstLastKlines = firstKline

                    axios.get('http://scrapper'+this.$store.state.apis_domain+'/klines/get/last/'+this.period+'/'+this.symbol)
                        .then(response => {
                            
                            let lastKline = this.formatDate(JSON.parse(response.data))
                            this.firstLastKlines = this.firstLastKlines.concat(lastKline)
                            this.columns = Object.keys(this.firstLastKlines[0])
                        })
                        .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
                })
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
        },
    },
    mounted(){
        this.getFirstLastKlines()
    }
}
</script>