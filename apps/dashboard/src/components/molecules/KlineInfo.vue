<template>
    <div v-if="Object.keys(kline).length > 0">
        {{ kline }}
    </div>
    <div v-else>
        <Loading />
    </div>
</template>

<script>
import Loading from '../atoms/Loading.vue'

export default {
    name: 'kline-info',
    components: {
        Loading
    },
    props: {
        kline: {
            type: Object,
            required: true
        }
    }
}
</script>