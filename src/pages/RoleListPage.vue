<template>
  <div class="row">
    <div class="col-md-12 col-xs-12">
      <p class="headers q-mt-lg"> دسترسی های ایحاد شده</p>
    </div>
  </div>
  <div class="row q-mt-lg">
    <div class="col-md-7 col-xs-12  q-pa-md">
      <table class="q-table q-table--bordered q-table--dense q-table--grid q-table--flat" style="font-size: 10pt">
        <thead class="bg-grey-1">
        <tr>
          <td style="width: 10%">ردیف</td>
          <td style="width: 20%">نام نقش</td>
          <td style="width: 15%">مشاهده</td>
          <td style="width: 15%">فعال سازی</td>
          <td style="width: 15%">غیر فعال سازی</td>
          <td style="width: 25%">وضعیت</td>
          <!--          <td style="width: 15%">ویرایش</td>-->
        </tr>
        </thead>
        <thead>
        <tr v-for="(item , index ) in roles.list" :key="index">
          <td style="width: 10%">{{ index + 1 }}</td>
          <td style="width: 20%">{{ item.name }}</td>
          <td style="width: 15%">
            <q-btn @click="seen(item.id , item.name)" label="مشاهده" class="full-width" color="teal" dense
                   text-color="white"></q-btn>
          </td>
          <td style="width: 15%">
            <q-btn :disable="item.active" @click="activation(item.id   , true)" label="فعالسازی" class="full-width"
                   color="orange-6" dense
                   text-color="dark"></q-btn>
          </td>
          <td style="width: 15%">
            <q-btn :disable="!item.active" @click="activation(item.id   , false)" label="غیر فعالسازی"
                   class="full-width" color="deep-orange-9" dense
                   text-color="white"></q-btn>
          </td>
          <td style="width: 25%">
            <template v-if="item.active">
              <p> نقش در وضعیت فعال می باشد</p>
            </template>
            <template v-else>
              <p> نقش در وضعیت غیر فعال می باشد</p>
            </template>

          </td>
          <!--          <td style="width: 15%">-->
          <!--            <q-btn label="ویرایش" class="full-width" color="yellow-9" dense text-color="dark"></q-btn>-->
          <!--          </td>-->
        </tr>
        </thead>
      </table>
    </div>
    <div class="col-md-5 col-xs-12 q-pa-md">
      <p class="headers">{{ one_role.name }}</p>
      <q-tree
        style="direction: ltr"
        :nodes="one_role.data"
        node-key="label"
        tick-strategy="none">

      </q-tree>
    </div>
  </div>

  <!--  -->
  <q-dialog
    style="direction: rtl"
    v-model="activated.selected"


  >
    <q-card style="width: 300px">
      <q-card-section>
        <div class="text-h6 headers text-dark">هشدار</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="row">
          <div class="col-md-12">
            <div class="full-width q-mt-lg">
              <template v-if="activated.active">
                <p class="text full-width q-pa-lg bg-green-2 text-dark">{{ activated.message }} </p>
              </template>
              <template v-else>
                <p class="text full-width q-pa-lg bg-pink-2 text-dark">{{ activated.message }} </p>
              </template>
            </div>
          </div>
          <div class="full-width q-mt-lg">
            <q-btn class="inputs" color="indigo-10" @click="active_btn(activated.id , activated.active)"
                   label="ثبت تغییرات"></q-btn>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="left" class="bg-white text-pink-6">
        <q-btn flat label="خروج" v-close-popup class="text"/>
      </q-card-actions>
    </q-card>
  </q-dialog>

</template>

<script>
import urls from "src/Urls";
import {reactive} from "vue";
import axios from "axios";
import {useQuasar} from "quasar";

export default {
  name: "Role_list_page",

  data() {
    const address = new urls()
    const $q = useQuasar()
    const roles = reactive({
      list: []
    })
    const one_role = reactive({
      name: '',
      data: [],
      id: '',
    })
    const activated = reactive({
      active: undefined,
      message: '',
      id: '',
      selected: false
    })

    function start() {
      axios.get(address.role_list()).then(response => {
        roles.list.splice(0, roles.list.length)
        for (let i = 0; i < response.data.data.length; i++) {
          roles.list.push({
            name: response.data.data[i].name,
            active: response.data.data[i].active,
            id: response.data.data[i].id,
            items: response.data.data[i].items
          })
        }
      }).catch(() => {
        $q.notify({
          position: 'bottom',
          timeout: 1500,
          message: 'خطا در دریافت اطلاعات',
          color: 'pink-6',
          textColor: "white",
          classes: 'notify_center',
        })
      })
    }

    start()
    return {
      activated,
      address,
      one_role,
      roles,
      start,
      toast(text, color, text_color) {
        $q.notify({
          position: 'bottom',
          timeout: 1500,
          message: text,
          color: color,
          textColor: text_color,
          classes: 'notify_center',
        })
      },
    }

  },

  methods: {

    seen(id, name) {
      this.one_role.name = name
      this.one_role.id = id
      const Tag = []
      this.one_role.data.splice(0, this.one_role.data.length)
      Tag.splice(0, Tag.length)
      axios.get(this.address.role_list() + '/' + id).then(
        response => {
          for (let i = 0; i < response.data.items.length; i++) {
            if (!Tag.includes(response.data.items[i].TagName)) {
              Tag.push(Tag.includes(response.data.items[i].TagName))
              this.one_role.data.push({
                label: response.data.items[i].TagName,
                children: [{
                  label: response.data.items[i].summary
                }]
              })
            } else {
              for (let j = 0; j < this.one_role.data.length; j++) {
                if (this.one_role.data[j].label === response.data.items[i].TagName) {
                  this.one_role.data[j].children.push
                  {
                    label: response.data.items[i].summary
                  }
                  break
                }

              }
            }

          }
        }
      ).catch(
        () => {
          this.toast('خطای داخلی سرور', 'pink-6', 'white')
        }
      )
    },
    activation(id, active) {
      this.activated.selected = true
      this.activated.active = active
      this.activated.id = id
      if (active) {
        this.activated.message = 'آیا از فعالسازی مطمین هستید ؟ '
      } else {
        this.activated.message = 'آیا از غیر فعال شدن مطمین هستید ؟'
      }
    },
    active_btn(id, fun) {
      if (!fun) {
        axios.delete(this.address.role_deleted(), {
          data: {
            id: id
          }
        }).then(res => {
          if (res.data.Done) {
            this.one_role.id = ''
            this.one_role.name = ''
            this.one_role.data = []
            this.activated.id = ''
            this.activated.active = undefined
            this.activated.selected = false
            this.activated.message = ''

            this.start()
            this.toast('عملیات با موفقیت انجام شد', 'green-9', 'white')
          } else {
            this.toast('خطای داخلی سرور', 'pink-6', 'white')
          }

        }).catch(
          () => {
            this.toast('خطای داخلی سرور', 'pink-6', 'white')
          }
        )
      } else {
        axios.patch(this.address.role_activated(), {
            id: id
        }).then(res => {
          if (res.data.Done) {
            this.one_role.id = ''
            this.one_role.name = ''
            this.one_role.data = []
            this.activated.id = ''
            this.activated.active = undefined
            this.activated.selected = false
            this.activated.message = ''

            this.start()
            this.toast('عملیات با موفقیت انجام شد', 'green-9', 'white')
          } else {
            this.toast('خطای داخلی سرور', 'pink-6', 'white')
          }

        }).catch(
          () => {
            this.toast('خطای داخلی سرور', 'pink-6', 'white')
          }
        )
      }
    }
  }
}
</script>

<style scoped>
.headers {
  font-size: 13pt;
  text-align: center;
  width: 100%;
  font-family: Ahang_b;
}

.text {
  font-family: iransans_r;
  font-size: 10pt;
  text-align: center;

}

.inputs {
  font-family: iransans_b;
  font-size: 10pt;
  text-align: right;
  width: 70%;
  margin-right: 15%;
  margin-left: 15%;
}

.labels {
  font-family: iransans_r;
  font-size: 9pt;
  text-align: right;
  width: 70%;
  margin-right: 15%;
  margin-left: 15%;
  color: #545454;
}

thead {
  font-family: iransans_b;
}

tbody {
  font-family: iransans_r;
}

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  text-align: center;
}

</style>
