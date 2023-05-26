<template>
    
    <PrimeCard>
        
        <template #content>

            <div class="card flex flex-wrap gap-3 p-fluid">
                
                <slot></slot>
                
                <div class="flex-auto">
                    <label class="text-sm block mb-2">Start date</label>
                    <PrimeCalendar v-model="startDate" class="mr-2" :placeholder="startDate.toLocaleDateString('en-US')" showIcon />
                </div>
                
                <div class="flex-auto">
                    <label class="text-sm block mb-2">End date</label>
                    <PrimeCalendar v-model="endDate" :placeholder="endDate.toLocaleDateString('en-US')" showIcon />
                </div>
                
                <div class="flex-auto">
                    <label class="text-sm block mb-2">&nbsp;</label>
                    <PrimeButton label="Plot" :loading="plotting" @click="plotFunction(startDate,endDate)" :disabled="(startDate >= endDate) || !plotCondition"></PrimeButton>
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
            startDate: new Date("8/1/2017"),
            endDate: new Date()
        }
    }
}
</script>