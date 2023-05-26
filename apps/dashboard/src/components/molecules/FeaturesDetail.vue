<template>
    <PrimeDataTable :value="fmtFeatures()" stripedRows>
        <PrimeColumn field="name" header="Name">
            <template #body="slotProps">
                <strong>{{ slotProps.data.name }}</strong>
            </template>
        </PrimeColumn>
        <PrimeColumn field="args" header="Args">
            <template #body="slotProps">
                <PrimeTag v-for="(value,arg) in slotProps.data.args" :key="arg" severity="warning" class="m-2">
                    <span class="ml-2 mr-2 font-medium">{{ arg }}</span>
                    <span class="primary-dark w-2rem h-2rem flex align-items-center justify-content-center">{{ value }}</span>
                </PrimeTag>
            </template>
        </PrimeColumn>
        <PrimeColumn field="klines_args" header="Klines Args">
            <template #body="slotProps">
                <PrimeTag v-for="klines_arg in slotProps.data.klines_args" :key="klines_arg" severity="danger" class="m-2" >
                    <span class="ml-2 mr-2 font-medium">{{ klines_arg }}</span>
                </PrimeTag>
            </template>
        </PrimeColumn>
        <PrimeColumn field="lag" header="Lag">
            <template #body="slotProps">
                <PrimeBadge v-for="lag in slotProps.data.lag" :key="lag" :value="lag" size="large" severity="info" />
            </template>
        </PrimeColumn>
    </PrimeDataTable>
</template>

<script>

export default {
    name: 'features-detail',
    props: {
        features: {
            type: Object,
            required: true
        }
    },
    methods: {
        fmtFeatures(){
            let features = []
            Object.keys(this.features).forEach((featureName)=>{
                let feature = this.features[featureName]
                features.push({name:featureName,args:feature.args,klines_args:feature.klines_args})
            })
            return features
        }
    }
}
</script>