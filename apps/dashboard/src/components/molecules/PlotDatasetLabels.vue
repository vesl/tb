<template>
    <PrimeCard>
        <template #title>Plot Labels</template>
        <template #content>
            <PlotForm :plotFunction="plotFunction" :plotting="plotting">
                <SelectPeriod v-model:period.sync="period" />
            </PlotForm>
            <PrimeProgressSpinner v-if="plotting" />
            <div v-if="labels">
                <h3>Count<PrimeTag severity="success" :value="labels.count" class="ml-3" /></h3>
                <h3>Repartition</h3>
                <PrimeChart type="bar" :data="labels.repartition" :options="labels.repartition_options" class="h-30rem" />
                <h3>Labels markers</h3>
                <PlotKlines :period="period" :symbol="$route.params.symbol" :markers="labels.markers" class="h-50rem" />
            </div>
        </template>
    </PrimeCard>
</template>

<script>
import SelectPeriod from "@/components/atoms/SelectPeriod.vue"
import PlotKlines from "@/components/molecules/PlotKlines.vue"
import PlotForm from "@/components/atoms/PlotForm.vue"
import axios from "axios"

export default {
    name: 'plot-dataset-events',
    props: ['dataset'],
    components: {
        SelectPeriod,
        PlotKlines,
        PlotForm
    },
    data(){
      return {
          period: this.$cookies.get("selectedPeriod") ? this.$cookies.get("selectedPeriod") : null,
          plotting: false,
          labels: null
      }  
    },
    methods: {
        plotFunction(start,end){
            this.labels = null
            this.plotting = true
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/labels/'+this.dataset+'/'+start+'/'+end+'/'+this.$route.params.symbol+'/historical')
                .then(response => {
                    this.labels = {}
                    this.labels.count = response.data.count
                    this.labels.repartition = {
                        labels: JSON.parse(response.data.repartition).index,
                        datasets: [{data: JSON.parse(response.data.repartition).data}]
                    }
                    this.labels.repartition_options = {plugins:{legend:{display:false}}}
                    let markers_start = JSON.parse(response.data.markers).map(marker => ({time: marker.time, text: marker.time.toString(16), position: 'belowBar', shape: 'arrowUp' , color: marker.side == 1 ? '#adffb1':'#ffb1ad'}))
                    let markers_end = JSON.parse(response.data.markers).map(marker => ({time: marker.first_touch, text: marker.time.toString(16), position: 'aboveBar', shape: 'arrowDown' , color: marker.side == 1 ? '#73bb3e':'#bb443e'}))
                    this.labels.markers = markers_start.concat(markers_end).sort((marker1,marker2)=>{ return marker1.time-marker2.time})
                    this.plotting = false
                })
                .catch(error => {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })
                    this.plotting = false
                    this.labels = null
                })
        }
    }
}
</script>