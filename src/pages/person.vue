<template>
  <div class="row">
    <div class="col-md-12 col-xs-12">
      <p class="headers q-mt-lg">ثبت افراد</p>
    </div>


  </div>
  <div class="row">
    <div class="col-md-5 col-xs-12">
      <div class="row">
        <div class="col-md-12 col-xs-12">
          <div class="full-width q-mt-lg">
            <label class="labels"> نام </label>
            <q-input v-model="data.name" type="text" maxlength="100" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>
        <div class="col-md-12 col-xs-12">
          <div class="full-width q-mt-lg">
            <label class="labels"> نام خانوادگی </label>
            <q-input v-model="data.family" type="text" maxlength="100" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>
        <div class="col-md-12 col-xs-12">
          <div class="full-width q-mt-lg">
            <label class="labels"> کد ملی </label>
            <q-input v-model="data.national_code" type="text" maxlength="100" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>
        <div class="col-md-12 col-xs-12">
          <div class="full-width q-mt-lg q-mb-md">
            <label class="labels"> درجه </label>
            <q-select v-model="data.grade_id" :loading="info.loading_grades" :options="info.grades" option-value="id"
                      option-label="name" dense color="green-9" outlined square
                      class="inputs" input-style="text-align: center"></q-select>
          </div>

        </div>
        <div class="col-md-12 col-xs-12">
          <div class="full-width q-mt-lg q-mb-md">
            <label class="labels"> قسمت مربوطه </label>
            <q-select v-model="data.position_id" :loading="info.loading_position"
                      :options="info.positions" option-value="id" option-label="name" dense color="green-9" outlined
                      square class="inputs" input-style="text-align: center ;">
            </q-select>
          </div>

        </div>
        <div class="col-md-12 col-xs-12">
          <div class="full-width q-mt-lg q-mb-md">
            <label class="labels"> دسترسی </label>
            <q-select v-model="data.role" :loading="info.loading_roles"
                      :options="info.roles" option-value="id" option-label="name" dense color="green-9" outlined
                      square class="inputs" input-style="text-align: center ;">
            </q-select>
          </div>

        </div>

        <div class="full-width q-mt-lg">
          <q-btn class="inputs" color="indigo-10" @click="save" label="ثبت افراد"></q-btn>
        </div>
      </div>

    </div>
    <div class="col-md-7 col-xs-12" style="border-right: 1px dashed black">
      <p class="text">افراد ثبت شده</p>
      <div class="row q-mt-md q-pa-md ">
        <q-input style="width: 80%" v-model="result.text" label="جستجو افراد" type="text" maxlength="100"
                 class="q-mt-md q-mb-md text col-md-9"
                 input-style="text-align: center"
                 square rounded label-color="black" color="green-9" outlined dense></q-input>
        <q-btn style="width: 20%" @click="search" label="مشاهده" type="text" maxlength="100"
               class="q-mt-md q-mb-md text col-md-3"
               input-style="text-align: center"
               square rounded label-color="black" color="green-9" outlined dense></q-btn>
        <table class="q-table q-ma-xs q-table--bordered q-table--dense q-table--grid q-table--flat"
               style="font-size: 10pt">
          <thead>
          <tr>
            <td style="width: 4%">ردیف</td>
            <td style="width: 10%">نام</td>
            <td style="width: 15%">نام خانوادگی</td>
            <td style="width: 15%">کد ملی</td>
            <td style="width: 10%">درجه</td>
            <td style="width: 10%">واحد</td>
            <td style="width: 10%">تاریخچه</td>
            <td style="width: 10%">نقش ها</td>
            <td style="width: 10%">ویرایش</td>
          </tr>
          </thead>
          <template v-if="!result.searched">
            <tbody v-show="!person_list.loading">
            <tr v-for="( item , index ) in person_list.data" :key="index">
              <td style="width: 5%">{{ index + 1 }}</td>
              <td style="width: 10%">{{ item.name }}</td>
              <td style="width: 15%">{{ item.family }}</td>
              <td style="width: 15%">{{ item.national_code }}</td>
              <td style="width: 12%">{{ item.position_name }}</td>
              <td style="width: 12%">{{ item.grade_name }}</td>
              <td style="width: 12%">
                <q-btn @click="history_btn(index)" class="full-width" dense square color="green-9"
                       label="تاریخچه"></q-btn>
              </td>
              <td style="width: 10%">
                <q-btn class="full-width" dense square color="info" text-color="dark" label="نقش ها"></q-btn>
              </td>
              <td style="width: 10%">
                <q-btn @click="update_show(index)" text-color="dark" class="full-width" dense square color="warning"
                       label="ویرایش"></q-btn>
              </td>
            </tr>
            </tbody>
            <tbody v-show="person_list.loading">
            <tr>
              <td colspan="9">درحال بروز رسانی</td>
            </tr>
            </tbody>
          </template>
          <template v-else>
            <tbody>
            <tr v-for="( item , index ) in result.res" :key="index">
              <td style="width: 5%">{{ index + 1 }}</td>
              <td style="width: 10%">{{ item.name }}</td>
              <td style="width: 15%">{{ item.family }}</td>
              <td style="width: 15%">{{ item.national_code }}</td>
              <td style="width: 12%">{{ item.position_name }}</td>
              <td style="width: 12%">{{ item.grade_name }}</td>
              <td style="width: 12%">
                <q-btn class="full-width" dense square color="green-9" label="تاریخچه"></q-btn>
              </td>
              <td style="width: 10%">
                <q-btn class="full-width" dense square color="info" text-color="dark" label="نقش ها"></q-btn>
              </td>
              <td style="width: 10%">
                <q-btn text-color="dark" class="full-width" dense square color="warning" label="ویرایش"></q-btn>
              </td>
            </tr>
            </tbody>
          </template>

        </table>
      </div>


    </div>
  </div>


  <q-dialog
    style="direction: rtl"
    v-model="history.history_dialog"
  >
    <q-card style="width: 600px">
      <q-card-section>
        <div class="text-h6 headers ">تاریخچه تغییرات</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <template v-if="history.history_list_name.length > 0">
          <table class="q-table q-table--bordered q-table--dense q-table--grid q-table--flat" style="font-size: 10pt">
            <thead class="bg-green-1">
            <tr>
              <td style="width: 40%">تاریخ</td>
              <td style="width: 60%">موضوع</td>
            </tr>
            </thead>
            <thead>
            <tr v-for="item in this.history.history_list_name">
              <td class="bg-yellow-1" style="width: 40%">{{ item.time }}</td>
              <td style="width: 60%">{{ item.describe }}</td>
            </tr>
            </thead>
          </table>
        </template>
        <template v-else>
          <p class="bg-warning text text-dark text-center full-width q-pa-lg">
            تغییراتی انجام نشده است
          </p>
        </template>

      </q-card-section>

      <q-card-actions align="left" class="bg-white text-pink-6">
        <q-btn flat label="خروج" v-close-popup class="text"/>
      </q-card-actions>
    </q-card>
  </q-dialog>


  <q-dialog
    style="direction: rtl"
    v-model="roles.role_dialog"
    full-width

  >
    <q-card style="width: 600px">
      <q-card-section>
        <div class="text-h6 headers "> مشاهده نقش</div>
      </q-card-section>

      <q-card-section class="q-pt-none">

      </q-card-section>

      <q-card-actions align="left" class="bg-white text-pink-6">
        <q-btn flat label="خروج" v-close-popup class="text"/>
      </q-card-actions>
    </q-card>
  </q-dialog>


  <q-dialog
    style="direction: rtl"
    v-model="update.dialog"
    full-width

  >
    <q-card style="width: 600px">
      <q-card-section>
        <div class="text-h6 headers ">تغییرات</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="row">
          <div class="col-md-12">
            <div class="full-width q-mt-lg">
              <label class="labels"> نام - {{ person_list.data[update.index].name }} </label>
              <q-input v-model="update.name" type="text" maxlength="100" input-style="text-align: center"
                       class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
            </div>
          </div>
          <div class="col-md-12">
            <div class="full-width q-mt-lg">
              <label class="labels"> نام خانوادگی - {{ person_list.data[update.index].family }} </label>
              <q-input v-model="update.family" type="text" maxlength="100" input-style="text-align: center"
                       class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
            </div>
          </div>
          <div class="col-md-12">
            <div class="full-width q-mt-lg">
              <label class="labels"> کد ملی - {{ person_list.data[update.index].national_code }}</label>
              <q-input v-model="update.national_code" type="text" maxlength="100" input-style="text-align: center"
                       class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
            </div>
          </div>
          <div class="col-md-12">
            <div class="full-width q-mt-lg q-mb-md">
              <label class="labels"> درجه - {{ person_list.data[update.index].grade_name }}</label>
              <q-select v-model="update.grade_id" :loading="info.loading_grades" :options="info.grades"
                        option-value="id"
                        option-label="name" dense color="green-9" outlined square
                        class="inputs" input-style="text-align: center"></q-select>
            </div>

          </div>
          <div class="col-md-12">
            <div class="full-width q-mt-lg q-mb-md">
              <label class="labels"> قسمت مربوطه - {{ person_list.data[update.index].position_name }} </label>
              <q-select v-model="update.position_id" :loading="info.loading_position"
                        :options="info.positions" option-value="id" option-label="name" dense color="green-9" outlined
                        square class="inputs" input-style="text-align: center ;">
              </q-select>
            </div>

          </div>
          <div class="col-md-12">
            <div class="full-width q-mt-lg q-mb-md">
              <label class="labels"> نقش مربوطه - {{ person_list.data[update.index].role_name }} </label>
              <q-select v-model="update.role" :loading="info.loading_roles"
                        :options="info.roles" option-value="id" option-label="name" dense color="green-9" outlined
                        square class="inputs" input-style="text-align: center ;">
              </q-select>
            </div>

          </div>

          <div class="full-width q-mt-lg">
            <q-btn class="inputs" color="indigo-10" @click="update_btn" label="ثبت تغییرات"></q-btn>
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
import {reactive} from "vue";
import axios from "axios";
import urls from "src/Urls";
import {useQuasar} from "quasar";


export default {
  name: "person",
  data() {

    const $q = useQuasar()
    const data = reactive({
      name: '',
      family: '',
      national_code: '',
      position_id: '',
      grade_id: '',
      role: ''

    })
    const info = reactive({
      positions: [],
      grades: [],
      roles: [],
      loading_position: true,
      loading_grades: true,
      loading_roles: true
    })
    const person_list = reactive({
      data: [],
      loading: true
    })
    const address = new urls()
    const result = reactive({
      searched: false,
      res: [],
      text: ''
    })
    const roles = reactive({
      index: -1,
      role_dialog: false,
      role_list_name: []
    })
    const history = reactive({
      index: -1,
      history_dialog: false,
      history_list_name: []
    })
    const update = reactive({
      index: -1,
      id: "",
      name: "",
      family: "",
      national_code: "",
      position_id: "",
      grade_id: "",
      role:'',
      dialog: false
    })
    const role_show = reactive([])

    function get_grade_position() {

      info.roles.splice(0, info.roles.length)
      info.grades.splice(0, info.grades.length)
      info.positions.splice(0, info.positions.length)
      axios.get(address.position_list()).then(response => {
        for (let i = 0; i < response.data.item.length; i++) {
          info.positions.push({
            name: response.data.item[i].name,
            id: response.data.item[i].id
          })
          info.loading_position = false
        }
      })
      axios.get(address.Grade_list()).then(response => {
        for (let i = 0; i < response.data.item.length; i++) {
          info.grades.push({
            name: response.data.item[i].name,
            id: response.data.item[i].id
          })
          info.loading_grades = false
        }
      })
      axios.get(address.role_list()).then(response => {
        for (let i = 0; i < response.data.data.length; i++) {
          info.roles.push({
            name: response.data.data[i].name,
            id: response.data.data[i].id
          })
          info.loading_roles = false
        }
      })
    }

    function lists() {
      axios.get(address.person_list()).then(response => {
        if (response.data.Done) {
          person_list.data.splice(0, person_list.data.length)
          for (let i = 0; i < response.data.data.length; i++) {
            person_list.data.push({
              "id": response.data.data[i].id,
              "name": response.data.data[i].name,
              "family": response.data.data[i].family,
              "national_code": response.data.data[i].national_code,
              "position_id": response.data.data[i].position_id,
              "position_name": response.data.data[i].position_name,
              "grade_name": response.data.data[i].grade_name,
              "grade_id": response.data.data[i].grade_id,
              "role": response.data.data[i].role,
              "active": response.data.data[i].active,
              "update_history": response.data.data[i].update_history,
              "last_update": response.data.data[i].last_update,
              "role_name":response.data.data[i].role_name


            })
          }
          person_list.loading = false
        } else {
          this.toast(response.data.ErrorMassage, 'pink-8', 'white')
        }

      })
    }

    lists()
    get_grade_position()

    return {
      role_show,
      update,
      history,
      roles,
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
      result,
      get_grade_position,
      person_list,
      lists,
      info,
      data
    }
  },
  methods: {
    save() {
      if (this.data.name !== '' && this.data.family !== ''
        && this.data.national_code !== '' && this.data.grade_id !== ''
        && this.data.position_id !== '') {

        const address = new urls()
        console.log(this.data)
        axios.post(address.person_create(), {
          "name": this.data.name,
          "family": this.data.family,
          "national_code": this.data.national_code,
          "position_id": this.data.position_id.id,
          "grade_id": this.data.grade_id.id,
          "role": this.data.role.id
        }).then(response => {
          if (response.data.Done) {
            this.toast('عملیات با موفقیت انجام شد', 'green-9', 'white')
            this.data.name = ''
            this.data.family = ''
            this.data.national_code = ''
            this.data.grade_id = ''
            this.data.position_id = ''
            this.data.role = ''
            this.lists()
          }
        })

      } else {
        this.toast('لطفا فیلد ها را کامل نمایید', 'pink-8', 'white')
      }
    },
    search() {
      if (this.result.text !== '') {
        const address = new urls()
        axios.get(address.person_list() + '/' + this.result.text).then(response => {
          if (response.data.Done) {
            this.result.res.splice(0, this.result.res.length)
            for (let i = 0; i < response.data.data.length; i++) {
              this.result.res.push({
                "name": response.data.data[i].name,
                "family": response.data.data[i].family,
                "national_code": response.data.data[i].national_code,
                "position_id": response.data.data[i].position_id,
                "position_name": response.data.data[i].position_name,
                "grade_name": response.data.data[i].grade_name,
                "grade_id": response.data.data[i].grade_id,
                "role": response.data.data[i].role,
                "active": response.data.data[i].active,
                "update_history": response.data.data[i].update_history,
                "last_update": response.data.data[i].last_update
              })


            }
            this.result.searched = true
            this.toast('اطلاعات بروز شده است', 'green-9', 'white')
          } else {
            this.toast(response.data.ErrorMassage, 'pink-8', 'white')
          }
        })
      } else {
        this.toast('اطلاعات تمام کاربران براساس فیلتر انجام شده در حال بروز رسانی می باشد', 'green-9', 'white')
        this.result.searched = false
      }

    },
    update_show(index) {
      this.update.index = index
      this.update.id = this.person_list.data[index].id
      this.update.dialog = true

    },
    update_btn() {
      const address = new urls()
      axios.put(address.person_update(), {
        "id": this.update.id,
        "name": this.update.name,
        "family": this.update.family,
        "national_code": this.update.national_code,
        "position_id": this.update.position_id.id,
        "grade_id": this.update.grade_id.id,
        "role":this.update.role.id
      }).then(response => {
        if (response.data.Done) {
          this.update.index = -1
          this.update.dialog = false
          this.lists()
          this.toast('عملیات با موفقیت انجام شد', 'green-9', 'white')
        } else {
          this.toast(response.data.ErrorMassage, 'pink-6', 'white')
        }
      })
    },
    history_btn(index) {
      console.log(this.person_list.data[index].update_history)
      this.history.history_dialog = true
      this.history.index = index
      this.history.history_list_name.splice(0, this.history.history_list_name.length)
      for (let i = 0; i < this.person_list.data[index].update_history.length; i++) {
        const day = new Date(this.person_list.data[index].update_history[i].update_at.toString());
        this.history.history_list_name.push({
          time: new persianDate(day).format('LLLL'),
          describe: this.person_list.data[index].update_history[i].describe
        })
      }
    },

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
