<template>
    <div class="col-10">
      <Title :title="title" />
    </div>
    <div class="col-2">
        <SymbolPicker />
    </div>
</template>

<script>
import Title from '../atoms/Title.vue'
import SymbolPicker from '../molecules/SymbolPicker.vue'

export default {
    name: 'header-content',
    components: {
        Title,
        SymbolPicker
    },
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>