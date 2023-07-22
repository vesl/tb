<template>
    <div class="flex flex-wrap" v-for="(value,key) in form" :key="key">
        <div class="col-6">
            <label class="text-sm block mb-2">{{ key }}</label>
        </div>
        <div class="col-6">
            <PrimeInputSwitch v-if="value.type == 'bool'" inputId="key" v-model="value.default" />
            <PrimeDropdown v-else-if="value.type == 'list'" v-model="value.default" :options="value.values" :placeholder="value.default" />
            <PrimeInputText v-else inputId="key" v-model="value.default" />
        </div>
    </div>
    <PrimeDivider />
    <div class="flex align-items-center justify-content-center">
        <PrimeButton type="button" :label="submitText" icon="pi pi-check" @click="submitFunction" :loading="loading" />
    </div>
</template>

<script>
export default {
    name: 'form-object',
    props: ['object','submitText','submitFunction','loading'],
    data(){
        return {
            form: this.object,
        }
    },
    methods: {
        submit(){
            this.form.submit = true
            this.$emit('object', this.form);
        }
    }
}
</script>