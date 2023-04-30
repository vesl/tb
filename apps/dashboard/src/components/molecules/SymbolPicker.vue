<template>
    <div class="pt-3">
        <FormSelect :items="symbols" :action="switchSymbol" :labelIcon="'bi-currency-exchange'" :selected="$route.params.symbol" />
    </div>
</template>

<script>
import FormSelect from './FormSelect.vue'

export default {
    name: 'symbol-picker',
    components: {
        FormSelect
    },
    data (){
        return {
            symbols: [
                {name:'BTCUSDT',value:'BTCUSDT'},
                {name:'BTCBUSD',value:'BTCBUSD'},
                {name:'ETHUSDT',value:'ETHUSDT'},
            ]
        }
    },
    methods: {
        switchSymbol(event){
            this.$router.push('/'+this.$route.params.app+'/'+this.$route.params.view+'/'+event.target.value)
        }
    }
}
</script>