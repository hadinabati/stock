<template>
  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style>
@font-face {
  font-family: iransans_r;
  src: url(src/fonts/IRANSansX-Regular.woff);
}
@font-face {
  font-family: iransans_b;
  src: url(src/fonts/IRANSansX-Bold.woff);
}
@font-face {
  font-family: Ahang_r;
  src: url(src/fonts/Ahang-Regular.woff);
}
@font-face {
  font-family: Ahang_b;
  src: url(src/fonts/Ahang-Black.woff);
}
.notify_center{
  font-family: iransans_b;
  font-size: 11pt;
  text-align: center;
  padding: .5rem;
  width: 40% ;
  margin-right: 30%;
  margin-left: 30%;

}
span{
  font-family: iransans_r;
  text-align: center;
}
</style>
