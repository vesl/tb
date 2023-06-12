<template>

    <div class="p-3">
        <KlinesTable v-for="period in $store.state.periods" :key="period" :period="period" :symbol="symbol" />
        <PlotKlines v-for="period in $store.state.periods" :key="period" :period="period" :symbol="symbol" />
    </div>

</template>

<script>
import KlinesTable from '@/components/molecules/KlinesTable.vue'
import PlotKlines from '@/components/molecules/PlotKlines.vue'

export default {
    name: 'scrapper-klines',
    components: {
      KlinesTable,
      PlotKlines
    },
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
    }
}
</script>