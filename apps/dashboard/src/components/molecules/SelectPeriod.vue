<template>
    <div class="flex-auto">
        <label class="text-sm block mb-2">Period</label>
        <PrimeDropdown v-model="selectedPeriod" :options="$store.state.periods" placeholder="Select a period" class="mr-2" />
    </div>
</template>

<script>
export default {
    props: ['period'],
    data(){
        return {
            selectedPeriod: this.period
        }
    },
    watch: {
        selectedPeriod(period) {
            this.$emit('update:period', period)
            this.$cookies.set('selectedPeriod', period)
        }
    }
}
</script>