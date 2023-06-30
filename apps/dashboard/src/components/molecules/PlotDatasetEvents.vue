<template>
    <PrimeCard>
        <template #title>Plot Events</template>
        <template #content>
            <PlotForm :plotFunction="plotFunction" :plotting="plotting">
                <SelectPeriod v-model:period.sync="period" />
            </PlotForm>
            <PrimeProgressSpinner v-if="plotting" />
            <div v-if="events">
                <h3>Count<PrimeTag severity="success" :value="events.count" class="ml-3" /></h3>
                <h3>Repartition</h3>
                <PrimeChart type="bar" :data="events.repartition" :options="events.repartition_options" class="h-30rem"  />
                <h3>Events markers</h3>
                <PlotKlines :period="period" :symbol="$route.params.symbol" :markers="events.markers" />
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
          events: null
      }  
    },
    methods: {
        plotFunction(start,end){
            this.events = null
            this.plotting = true
            axios.get('http://trainer'+this.$store.state.apis_domain+'/datasets/get/events/'+this.dataset+'/'+start+'/'+end+'/'+this.$route.params.symbol+'/historical')
                .then(response => {
                    this.events = {}
                    this.events.count = response.data.count
                    this.events.repartition = {
                        labels: JSON.parse(response.data.repartition).index,
                        datasets: [{data: JSON.parse(response.data.repartition).data}]
                    }
                    this.events.repartition_options = {plugins:{legend:{display:false}}}
                    this.events.markers = JSON.parse(response.data.markers).map(marker => ({time: marker.time, text: marker.type, position: 'aboveBar', shape: 'circle' , color: '#ceecf5'}))
                    this.plotting = false
                })
                .catch(error => {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })
                    this.plotting = false
                    this.events = null
                })
        }
    }
}
</script>