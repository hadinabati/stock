<template>
  <q-layout  view="hHh lpR fFf">

    <q-header style="height: 40px" reveal elevated bordered  class="text-white bg-primary" >
      <q-toolbar  >
        <q-toolbar-title  class="headers">
          سامانه انبار داری فاوا
        </q-toolbar-title>
        <q-btn  dense flat round  icon="menu" @click="toggleRightDrawer" />

      </q-toolbar>
    </q-header>

    <q-drawer width="50" mini-width="50" :mini="true" show-if-above v-model="rightDrawerOpen" side="right" bordered>
     <q-btn icon="home" flat class="full-width q-mt-md q-mb-xs">
       <q-tooltip class="menus bg-primary" style="font-family: iransans_r">
         خانه
       </q-tooltip>
     </q-btn>
      <q-btn icon="store" flat class="full-width q-mt-md q-mb-xs">
        <q-tooltip class="menus bg-primary" style="font-family: iransans_r">
          ثبت کالا
        </q-tooltip>
      </q-btn>
    </q-drawer>

    <q-page-container>
      <router-view style="direction: rtl" />
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    const rightDrawerOpen = ref(false)

    return {
      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      }
    }
  }
}
</script>

<style scoped>
.headers{
  font-family: Ahang_b;
  font-size: 10pt;
  line-height: 40px;
  text-align: center;
}
.menus{
  font-size: 11pt;
  font-family: iransans_b;


}
</style>
