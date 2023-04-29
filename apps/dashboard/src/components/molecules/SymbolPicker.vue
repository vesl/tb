<template>
    <div class="pt-3">
        <FormSelect :items="symbols" :action="switchSymbol" :labelIcon="labelIcon" />
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
            labelIcon: 'bi-currency-exchange',
            symbols: [
                {name:'BTCUSDT',value:'BTCUSDT'},
                {name:'BTCBUSD',value:'BTCBUSD'},
                {name:'ETHUSDT',value:'ETHUSDT'},
            ]
        }
    },
    methods: {
        switchSymbol(event){
            console.log(event.target.value)
            this.$store.commit('switchSymbol',event.target.value)
        }
    }
}
</script>