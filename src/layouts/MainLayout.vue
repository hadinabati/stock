<template>
  <q-layout view="lHh Lpr lFf" style="direction: rtl">
    <q-header elevated >
      <q-toolbar>
        <q-btn class="headers" flat dense label="خانه"   @click="this.change_route('/')"></q-btn>
        <q-btn class="headers" flat  dense  label="ثبت " style="width: 8rem">
        <q-menu fit >
          <q-list style="min-width: 100px">
            <q-item clickable v-close-popup>
              <q-item-section @click="this.change_route('stock')" class="sub_headers">ثبت کالا</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section class="sub_headers" @click="this.change_route('Position')">ثبت واحد</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section class="sub_headers" @click="this.change_route('person')">ثبت افراد</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section class="sub_headers" @click="this.change_route('Grade')">ثبت درجات نظامی</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section class="sub_headers"  @click="this.change_route('Category')">ثبت دسته بندی</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
        </q-btn>
        <q-btn class="headers" flat  dense  label="مشاهده " style="width: 8rem">
          <q-menu fit >
            <q-list style="min-width: 100px">
              <q-item clickable v-close-popup>
                <q-item-section @click="this.change_route('products')" class="sub_headers">مشاهده کالا</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn class="headers" flat dense label="دسترسی ها" style="width: 8rem">
          <q-menu fit >
            <q-list style="min-width: 100px">
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('create_role')">ایجاد دسترسی</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('role_list')">دسترسی های ثبت شده</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn class="headers" flat dense label="فعالیت " style="width: 8rem">
          <q-menu fit >
            <q-list style="min-width: 100px">
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('repair')">ثبت گردشکار</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('repair')">لیست گردش کار های ثبت شده</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('activity_create')">ثبت نوع گردشکاری</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('activity_list')">لیست نوع گردشکاری</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn class="headers" flat dense label="گزارشات" style="width: 8rem">
          <q-menu fit >
            <q-list style="min-width: 100px">
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers">گزارشات کالا</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('')">گزارشات افراد</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('')">گزارشات واحد ها</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers" @click="this.change_route('')">گزارشات درجات</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers"  @click="this.change_route('')">گزارشات دسته بندی</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section class="sub_headers"  @click="this.change_route('')">گزارشات فعالیت های روزانه</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn flat dense  class="absolute-left" label="مشخصات">
          <q-menu>
            <div class="row no-wrap q-pa-md ">
              <div class="column">
                <div class="text-h6 q-mb-md" style="font-family: iransans_b">تنظیمات</div>
                <q-btn
                  color="pink-6"
                  label="خروج"
                  style="font-family: Ahang_r"
                  push
                  size="sm"
                  v-close-popup
                />
              </div>

              <q-separator vertical inset class="q-mx-lg" />

              <div class="column items-center">
                <q-avatar size="72px">
                  <img src="https://cdn.quasar.dev/img/avatar4.jpg">
                </q-avatar>

                <div style="font-family: iransans_r" class="text-subtitle2 q-mt-md q-mb-xs">هادی نباتی</div>
                <div style="font-family: iransans_r" class="text-subtitle2 q-mt-md q-mb-xs">کاربر عادی</div>

              </div>
            </div>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>
      <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'



export default defineComponent({
  name: 'MainLayout',
  data () {
    const leftDrawerOpen = ref(false)
    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  },
  methods:{
    change_route(route){
     this.$router.push(route)
    }
  }
})
</script>
<style>
.headers{
  font-family: Ahang_b;
  font-size: 13pt;


}
.sub_headers{
  font-family: Ahang_r;
  font-size: 12pt;
}
</style>
