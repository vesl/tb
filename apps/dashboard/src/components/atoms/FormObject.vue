<template>
    <div class="flex flex-wrap" v-for="(value,key) in form" :key="key">
        <div class="col-6">
            <label class="text-sm block mb-2">{{ key }}</label>
        </div>
        <div class="col-6">
            <PrimeInputSwitch v-if="value.type == 'bool'" :inputId="key" v-model="value.value" />
            <PrimeDropdown v-else-if="value.type == 'list'" v-model="value.value" :options="value.values" :placeholder="value.value" />
            <PrimeInputText v-else inputId="key" v-model="value.value" />
        </div>
    </div>
    <PrimeDivider />
    <div class="flex align-items-center justify-content-center">
        <PrimeButton type="button" :label="submitText" icon="pi pi-check" @click="submitFunction(form)" :loading="loading" />
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
    }
}
</script>