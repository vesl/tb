<template>
    <table class="table table-dark table-bordered table-striped">
        <tbody>
            <tr>
                <td scope="col" v-for="(value,key) in kline" :key="key">{{ $stringFunctions.firstLetterUpper(key) }}</td>
            </tr>
            <tr>
                <td v-for="(value,key) in kline" :key="key">{{ (key == "open_time" || key == "close_time") ? new Date(value).toUTCString() : value }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>

export default {
    name: 'kline-detail',
    props: {
        kline: {
            type: Object,
            required: true
        }
    }
}
</script>