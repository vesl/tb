<template>
    <PrimeCard>
        <template #title>Plot features</template>
        <template #content>
            <PlotForm :plotFunction="plotFunction" :plotting="plotting" :plotCondition="(Boolean(period) && Boolean(featuresMap))">
                <SelectFeaturesMap v-model:featuresMap.sync="featuresMap" :dataset="dataset" />
                <SelectPeriod v-model:period.sync="period" />
            </PlotForm>
            <PrimeProgressSpinner v-if="plotting" />
            <div v-if="Object.keys(plotData).length && !plotting">
                <div v-for="feature in Object.keys(plotData)" :key="feature">
                    <PrimeDivider />
                    <PrimeTag severity="success" class="p-2 mb-2">{{ feature }}</PrimeTag>
                    <LWChart type="line" :data="plotData[feature]" />
                </div>
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import SelectFeaturesMap from "@/components/molecules/SelectFeaturesMap.vue"
import SelectPeriod from "@/components/atoms/SelectPeriod.vue"
import PlotForm from "@/components/atoms/PlotForm.vue"
import LWChart from "@/components/atoms/LWChart.vue"
import axios from "axios"

export default {
    name: 'plot-dataset-features',
    props: ['dataset'],
    components: {
        SelectFeaturesMap,
        SelectPeriod,
        PlotForm,
        LWChart
    },
    data(){
      return {
          period: this.$cookies.get("selectedPeriod") ? this.$cookies.get("selectedPeriod") : null,
          featuresMap: null,
          plotting: false,
          plotData: {}
      }  
    },
    methods: {
        plotFunction(start,end){
            this.plotting = true
            this.plotData = {}
            axios.post('http://trainer'+this.$store.state.apis_domain+'/features/plot/'+start+'/'+end+'/'+this.$route.params.symbol+'/'+this.period,this.featuresMap,{headers:{'Content-Type':'application/json'}})
                .then(response => {
                    let data = JSON.parse(response.data)
                    Object.keys(data[0]).forEach((feature) => {
                        if (feature == 'time') return
                        this.plotData[feature.split('!')[0]] = data.map( record => { 
                            return { time: record.time, value: record[feature] }
                        })
                    })
                    this.plotting = false
                })
                .catch(error => {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })
                    this.plotting = false
                }) 
        }
    }
}
</script>