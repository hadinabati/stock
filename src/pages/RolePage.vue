<template>
  <div class="row">
    <p class="headers full-width q-ma-lg"> ایجاد دسترسی</p>
    <div class="col-md-3"></div>
    <div class="col-md-6 col-xs-12">
      <div class="full-width q-mt-lg">
        <label class="labels"> نام دسته بندی </label>
        <q-input type="text" maxlength="100" input-style="text-align: center" v-model="info.name"
                 class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
      </div>
      <div class="full-width q-mt-lg">
        <label class="labels"> دسترسی ها </label>
        <q-tree style="direction: ltr" class="col-12 col-xs-12"
                :nodes="info.routes"
                node-key="id"
                tick-strategy="strict"
                v-model:ticked="route_chose"
                label-key="label"
        >
        </q-tree>
      </div>
      <div class="col-md-6">
        <label class="labels"> </label>
        <q-btn @click="insert" label="ثبت" class="inputs q-mb-lg"
               style="width: 60% ; margin-left: 20% ; margin-right: 20%"
               rounded label-color="white" color="light-blue-10" outlined dense></q-btn>
      </div>
    </div>
    <div class="col-md-3 col-xs-12">
      <q-btn class="text absolute-bottom full-width q-mt-lg " @click="update" style="height: 80px" color="grey-10"
             text-color="white" label="بروز رسانی"></q-btn>
    </div>

  </div>
</template>

<script>
import {reactive} from "vue";
import urls from "src/Urls";
import axios from "axios";
import {useQuasar} from "quasar";

export default {
  name: "RolePage",
  data() {
    const $q = useQuasar()
    const route_chose = reactive([])
    const info = reactive({
      name: '',
      routes: [],
    })
    const address = new urls()
    let Tag = []

    function Routes() {
      axios.get(address.route_list()).then(response => {
        if (response.status === 200) {
          Tag.splice(0, Tag.length)
          info.routes.splice(0, info.routes.length)
          for (let i = 0; i < response.data.data.length; i++) {
            if (!Tag.includes(response.data.data[i].TagName)) {
              Tag.push(response.data.data[i].TagName)
              info.routes.push({
                label: response.data.data[i].TagName,
                children: [{
                  label: (i + 1).toString() + ' -  ' + response.data.data[i].TagName + '/' + response.data.data[i].summary,
                  id: response.data.data[i].id
                }]
              })

            } else {
              for (let j = 0; j < info.routes.length; j++) {
                if (info.routes[j].label === response.data.data[i].TagName) {
                  info.routes[j].children.push({
                    label: (i + 1).toString() + ' -  ' + response.data.data[i].TagName + '/' + response.data.data[i].summary,
                    id: response.data.data[i].id
                  })
                  break
                }
              }
            }
          }


        }
      })
    }


    Routes()
    return {
      Routes,
      info,
      address,
      route_chose,
      Tag,
      toast(text, color, text_color) {
        $q.notify({
          position: 'bottom',
          timeout: 1500,
          message: text,
          color: color,
          textColor: text_color,
          classes: 'notify_center',
        })
      }
    }
  },

  methods: {
    insert() {
      if (this.info.name !== '') {
        if (this.route_chose.length === 0 || this.route_chose.includes(undefined)) {
          this.toast('می بایست تنها روی زیر منو ها کلیک کنید ', 'pink-6', 'white')
        } else {
          axios.post(this.address.role_create(), {
            "name": this.info.name,
            "items": this.route_chose
          }).then(response => {
            if (response.data.Done) {
              this.toast('اطلاعات با موفقیت درج شدتد', 'green-9', 'white')
            } else {
              this.toast(response.data.ErrorMessage, 'pink-6', 'white')
            }
          }).catch(() => {
            this.toast('خطا در سرور', 'pink-6', 'white')
          })

        }

      } else {
        this.toast('لطفا قسمت نام را کامل کنید', 'pink-6', 'white')
      }
    },
    update() {
      axios.post(this.address.route_update()).then(res => {
        if (res.data.Done) {
          this.Routes()
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
