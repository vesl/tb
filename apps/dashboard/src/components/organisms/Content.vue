<template>
    <div class="row shadow">
        <Header :title="$stringFunctions.firstLetterUpper(app) +' '+$stringFunctions.firstLetterUpper(view)" />
    </div>
    <!-- on met le header  / skeleton etc .. puis le composant dynamique -->
    https://stackoverflow.com/questions/44998790/how-to-load-a-component-from-a-variable-name-in-vue-js
    {{ $store.state.symbol }}
</template>

<script>
import Header from '../molecules/Header.vue'

export default {
    name: 'content-panel',
    components: {
        Header
    },
    computed: {
        app() {
            return this.$route.params.app
        },
        view() {
            return this.$route.params.view  
        },
    }
}
</script>