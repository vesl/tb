<template>
    <div class="primary col-2 shadow-2 z-1 p-5">
        <span class="font-medium">TB Dashboard</span>
    </div>
    <div class="secondary col-10 shadow-2 z-1 p-5">
        <span class="font-medium">{{ $stringFunctions.firstLetterUpper(app+' - '+view) }}</span>
    </div>
</template>

<script>

export default {
    name: 'header-panel',
    props: {
      app: {
          type: String,
          required: true
      },
      view: {
          type: String,
          required: true
      },
      symbol: {
          type: String,
          required: true
      }
    }
}
</script>