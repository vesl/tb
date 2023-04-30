<template>
    <div class="tb-middle-dark rounded m-2 shadow pb-3">
        <ContentHeader :title="'Last live kline'"/>
        <slot><Loading /></slot>
    </div>
</template>

<script>
import Loading from '../atoms/Loading.vue'
import ContentHeader from '../atoms/ContentHeader.vue'

export default {
    name: 'content-info',
    components: {
        ContentHeader,
        Loading
    },
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>