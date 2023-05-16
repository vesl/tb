<template>
    <table class="table table-dark table-bordered table-striped">
        <tbody>
            <tr v-for="(featureMap,feature) in featuresMap.features" :key="feature">
                <td>
                    {{ feature }}
                    <hr />
                    <table class="table table-light table-stripped">
                        <tbody>
                            <tr>
                                <td width="10%">Klines args</td>
                                <td width="90%">
                                    <button class="btn btn-primary disabled m-1" v-for="kline_arg in featureMap.kline_args" :key="kline_arg">{{ kline_arg }}</button>
                                </td>
                            </tr>
                            <tr>
                                <td width="10%">Args</td>
                                <td width="90%">
                                    <button class="btn btn-danger disabled m-1" v-for="(value,arg) in featureMap.args" :key="arg">{{ arg }} <Badge :text="value" :type="'dark'" /></button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import Badge from '../atoms/Badge.vue'

export default {
    name: 'features-map-detail',
    components : {
        Badge
    },
    props: {
        featuresMap: {
            type: Object,
            required: true
        }
    }
}
</script>