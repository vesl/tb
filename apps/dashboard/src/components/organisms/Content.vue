<template>
    <div class="row shadow">
        <Header :title="$stringFunctions.firstLetterUpper(app) +' '+$stringFunctions.firstLetterUpper(view)" />
    </div>
    <div class="row p-4">
        <component :is="currentComponent" :app="app" :view="view"/>
    </div>
</template>

<script>
import Header from '../molecules/Header.vue'
import ScrapperKlines from './ScrapperKlines.vue'

export default {
    name: 'content-panel',
    components: {
        Header,
        ScrapperKlines
    },
    computed: {
        app() {
            return this.$route.params.app
        },
        view() {
            return this.$route.params.view  
        },
        currentComponent(){
            return this.$stringFunctions.firstLetterUpper(this.app)+this.$stringFunctions.firstLetterUpper(this.view)
        }
    }
}
</script>