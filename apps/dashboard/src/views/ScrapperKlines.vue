<template>

    <div class="p-3">
        <KlinesTable v-for="period in $store.state.periods" :key="period" :period="period" :symbol="symbol" />
        <PrimeCard v-for="period in $store.state.periods" :key="period" class="mb-5">
            <template #title>Kline Plot - {{ period }}</template>
            <template #content>
                <PlotKlines :period="period" :symbol="symbol" />
            </template>
        </PrimeCard>
    </div>

</template>

<script>
import PlotKlines from '@/components/molecules/PlotKlines.vue'
import KlinesTable from '@/components/atoms/KlinesTable.vue'

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