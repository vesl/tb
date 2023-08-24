<template>
    <div class="flex flex-wrap align-items-center primary col-2 shadow-2 z-1 p-4">
        <span class="font-medium">TB Dashboard</span>
    </div>
    <div class="flex flex-wrap align-items-center secondary col-10 shadow-2 z-1 p-4">
        <span class="font-medium">{{ $string.firstLetterUpper(app+' - '+view) }}</span>
        <div class="absolute right-0">
            <PrimeDropdown v-model="selectedSymbol" :options="$store.state.symbols" :placeholder="symbol" class="mr-2" />
        </div>
    </div>
</template>

<script>

export default {
    name: 'header-panel',
    data(){
        return {
            selectedSymbol: null
        }
    },
    props: ['app','view','symbol'],
    watch: {
        selectedSymbol(symbol){
            this.$router.push({path: '/'+this.app+'/'+this.view+'/'+symbol})
        }
    }
}
</script>