<template>

    <div class="p-3">
        <PrimeCard>
            <template #title>Scrap talib features maps</template>
            <template #content>
                <PrimeButton type="button" label="Scrap" icon="pi pi-sync" :loading="scrapping" @click="scrapFeaturesMaps" />
            </template>
        </PrimeCard>
    </div>

</template>

<script>
import axios from 'axios'

export default {
    name: 'scrapper-talib',
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
    data (){
      return {
          scrapping : false
      }
    },
    methods: {
        scrapFeaturesMaps(){
            this.scrapping = true
            axios.get('http://scrapper'+this.$store.state.apis_domain+'/talib/scrap/features_maps')
                .then(response => {
                    this.scrapping = false
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: response.data, life: 3000 })
                })
                .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error })})
        }
    }
}
</script>