<template>
    <div class="pt-3">
        <FormSelect :items="featuresMapsNames" :action="selectFeaturesMap" :labelIcon="'bi-card-checklist'" :selected="selectedFeaturesMap" />
    </div>
</template>

<script>
import FormSelect from './FormSelect.vue'

export default {
    name: 'features-map-picker',
    components: {
        FormSelect
    },
    data(){
        return {
            selectedFeaturesMap: this.featuresMapsNames[0]
        }
    },
    props: {
        featuresMapsNames: {
            type: Array,
            required: true
        }
    },
    methods: {
        selectFeaturesMap(event){
            this.selectedFeaturesMap = event.target.value
        }
    }
}
</script>