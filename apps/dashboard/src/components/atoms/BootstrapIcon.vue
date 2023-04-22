<template>
    <i :class="[icon, 'p-1', 'bi']"></i>
</template>

<script>
export default {
  name: 'BootstrapIcon',
  props: {
    icon: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
</style>