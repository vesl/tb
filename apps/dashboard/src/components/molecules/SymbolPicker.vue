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
    computed: {
      symbols(){
          let symbols=[]
          this.$store.state.symbols.forEach((item)=>{
            symbols.push({name:item,value:item})  
          })
          return symbols
      }  
    },
    methods: {
        switchSymbol(event){
            this.$router.push('/'+this.$route.params.app+'/'+this.$route.params.view+'/'+event.target.value)
        }
    }
}
</script>