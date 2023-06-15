<template>
    <div class="card flex flex-wrap gap-3 p-fluid">
        <slot></slot>
        <div class="flex-auto">
            <label class="text-sm block mb-2">Start date</label>
            <PrimeCalendar v-model="start" class="mr-2" :placeholder="start.toString()" dateFormat="mm-dd-yy" showIcon />
        </div>
        <div class="flex-auto">
            <label class="text-sm block mb-2">End date</label>
            <PrimeCalendar v-model="end" :placeholder="end.toString()" dateFormat="mm-dd-yy" showIcon />
        </div>
        <div class="flex-auto">
            <label class="text-sm block mb-2">&nbsp;</label>
            <PrimeButton label="Plot" :loading="plotting" @click="plotFunction($string.formatDate(start),$string.formatDate(end))" :disabled="(start >= end) || !plotCondition"></PrimeButton>
        </div>
    </div>
</template>

<script>
export default {
    name: 'plot-form',
    props: {
      plotFunction: {
          type: Function,
          required: true
      },
      plotting: {
          type: Boolean,
          required: true
      },
      plotCondition: {
          type: Boolean,
          required: false,
          default: true
      }
    },
    data(){
        return {
            start: this.$cookies.get("start") ? new Date(this.$cookies.get("start")):new Date("08/01/2017"),
            end: this.$cookies.get("end") ? new Date(this.$cookies.get("end")):new Date(),
        }
    },
    watch: {
        start(start){
            this.$cookies.set("start",this.$string.formatDate(start))
        },
        end(end){
            this.$cookies.set("end",this.$string.formatDate(end))
        },
    }
}
</script>