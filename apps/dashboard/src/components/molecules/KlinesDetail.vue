<template>
    <PrimeDataTable :value="fmtKlines()">
        <PrimeColumn v-for="(column, index) in columns" :key="index" :field="column.field" :header="column.header"></PrimeColumn>
    </PrimeDataTable>
</template>

<script>

export default {
    name: 'klines-detail',
    props: {
        klines: {
            type: Object,
            required: true
        }
    },
    computed: {
      columns(){
          let columns = []
          Object.keys(this.klines[0]).forEach((col) => {
              columns.push({
                  field: col,
                  header: this.$stringFunctions.firstLetterUpper(col)
              })
          })
          return columns
      }  
    },
    methods: {
        fmtKlines(){
            let fmtKlines = []
            this.klines.forEach((kline)=>{
                Object.keys(kline).forEach((key)=>{
                    if(key == 'open_time' || key == 'close_time') kline[key] = new Date(kline[key]).toUTCString()
                })
                fmtKlines.push(kline)
            })
            return fmtKlines
        }
    }
}
</script>