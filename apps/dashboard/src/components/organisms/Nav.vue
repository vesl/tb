<template>
  <div v-for="(app,index) in $store.state.nav.apps" :key="index">
    <div class="text-sm font-light p-2 shadow-2">
      <i :class="app.icon" />
      {{ $string.firstLetterUpper(app.name) }}
    </div>
    <div v-for="(view, index) in app.views" :key="index" class="p-3 transition-duration-100" :class="getNavBtnClass(app,view)" @click="select(app.name,view.name)">
      {{ $string.firstLetterUpper(view.name) }}
    </div>
  </div>
</template>

<script>

export default {
  name: 'nav-panel',
  methods: {
    select(app,view) {
      this.$router.push('/'+app+'/'+view+'/'+(this.$route.params.symbol ? this.$route.params.symbol:this.$store.state.symbols[0]))
    },
    getNavBtnClass(app,view){
      return this.selectedApp == app.name && this.selectedView == view.name ? 'nav-btn-selected':'nav-btn'
    }
  },
  computed: {
    selectedApp(){
      return 'app' in this.$route.params ? this.$route.params.app:0
    },
    selectedView(){
      return 'view' in this.$route.params ? this.$route.params.view:0
    }
  }
}
</script>

<style scoped>
  .nav-btn:hover{
    cursor: pointer;
    background: var(--primary-900);
    border-left: 0.4em solid var(--green-500);
  }
  .nav-btn-selected {
    background: var(--primary-900);
    border-left: 0.4em solid var(--primary-300);
  }
</style>