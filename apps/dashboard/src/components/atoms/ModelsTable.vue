<template>
     <PrimeCard>
        <template #title>Trained models</template>
        <template #content>
            <PrimeDataTable v-if="models.length > 0" :value="models" stripedRows>
                <PrimeColumn v-for="column in Object.keys(models[0])" :key="column" :field="column" :header="column" sortable />
            </PrimeDataTable>
        </template>
    </PrimeCard>
</template>

<script>
import axios from "axios"

export default {
    name: 'models-table',
    props: ['symbol'],
    data(){
      return {
          models: {}
      }  
    },
    mounted(){
        axios.get('http://trainer'+this.$store.state.apis_domain+'/models/get/metadatas/'+this.symbol)
            .then(response => {this.models = response.data})
            .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
    }
}
</script>