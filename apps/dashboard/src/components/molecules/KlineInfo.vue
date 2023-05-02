<template>
    <div v-if="Object.keys(kline).length > 0">
        <table class="table table-dark table-bordered table-striped">
            <tbody>
            <tr>
                <td scope="col" v-for="(value,key) in kline">{{ $stringFunctions.firstLetterUpper(key) }}</td>
            </tr>
            <tr>
                <td v-for="(value,key) in kline">{{ (key == "open_time" || key == "close_time") ? new Date(value).toUTCString() : value }}</td>
            </tr>
            </tbody>
        </table>
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