<template>
    <i :class="[icon, 'p-1']"></i>
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