<template>
    
    <PrimeCard>
        
        <template #content>

            <div class="card flex flex-wrap gap-3 p-fluid">
                
                <slot></slot>
                
                <div class="flex-auto">
                    <label class="text-sm block mb-2">Start date</label>
                    <PrimeCalendar v-model="start" class="mr-2" :placeholder="$stringFunctions.formatDate(start)" dateFormat="mm-dd-yy" showIcon />
                </div>
                
                <div class="flex-auto">
                    <label class="text-sm block mb-2">End date</label>
                    <PrimeCalendar v-model="end" :placeholder="$stringFunctions.formatDate(end)" dateFormat="mm-dd-yy" showIcon />
                </div>
                
                <div class="flex-auto">
                    <label class="text-sm block mb-2">&nbsp;</label>
                    <PrimeButton label="Plot" :loading="plotting" @click="plotFunction($stringFunctions.formatDate(start),$stringFunctions.formatDate(end))" :disabled="(start >= end) || !plotCondition"></PrimeButton>
                </div>
        
            </div>
            
        </template>

    </PrimeCard>
    
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
            start: new Date("8/1/2017"),
            end: new Date()
        }
    }
}
</script>