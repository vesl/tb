<template>
    <div class="flex-auto">
        <label class="text-sm block mb-2">{{ title }}</label>
        <PrimeDropdown v-model="selected" :options="options" :placeholder="'Select a '+ title" class="mr-2" />
    </div>
</template>

<script>
import axios from "axios"

export default {
    name: 'select-api',
    props: ['app','uri','title','output'],
    data(){
        return {
            options: [],
            cookie_name: 'selected_'+this.app+this.uri.replaceAll('/','_')+'_type',
            selected: null,
        }
    },
    watch: {
        selected(option) {
            this.$emit("update:output", option)
            this.$cookies.set(this.cookie_name, option)
        },
    },
    mounted() {
        this.selected = this.$cookies.get(this.cookie_name) ? this.$cookies.get(this.cookie_name) : null
        axios.get('http://'+this.app+this.$store.state.apis_domain+this.uri)
            .then(response => {this.options = response.data})
            .catch(error => {this.$toast.add({ severity: 'error', summary: 'Error', detail: error, life: 3000 })})
    }
}
</script>