<template>
  <div class="row q-mt-lg">
    <div class="col-12">
      <p class="headers">ایجاد فرم گردشکار</p>
    </div>
  </div>
  <div class="row q-mt-lg">
    <div class="col-md-4"></div>
    <div class="col-md-4 col-xs-12">
      <div class="row">
        <div class="col-md-12">
          <div class="full-width q-mt-lg">
            <label class="labels">نام فعالیت</label>
            <q-input v-model="activity_info.name" type="text" maxlength="100" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>

        <div class="col-md-12">
          <div class="full-width q-mt-lg q-mb-md">
            <label class="labels"> دسته بندی</label>
            <q-select v-model="activity_info.category_id"
                      :loading="activity_info.loading"
                      :options="activity_info.category_list"
                      option-value="id" option-label="name" dense color="green-9" outlined
                      square class="inputs" input-style="text-align: center ;">
            </q-select>
          </div>

        </div>

        <div class="col-md-6">
          <div class="full-width q-mt-lg">
            <q-btn color="indigo-10" @click="Add" class="inputs" label="اضافه کردن قسمت"></q-btn>
          </div>
        </div>

        <div class="col-md-12">
          <div class="row">
            <template v-for="(item , index) in activity_info.properties" :key="index">
              <div class="q-mt-lg col-md-6 col-xs-8">
                <label class="labels">نام قسمت</label>
                <q-input v-model="activity_info.properties[index]" type="text" maxlength="100"
                         input-style="text-align: center"
                         class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>


              </div>
              <div class="q-mt-lg col-md-6  col-xs-4">
                <label class="labels"></label>
                <q-btn color="pink-6" @click="del(index)" dense class="inputs" label="حذف کردن قسمت"></q-btn>
              </div>
            </template>
          </div>

        </div>

      </div>
      <br>
      <hr>
      <q-btn class="q-mt-md inputs" color="green-9" @click="save" label="ذخیره داده" dense></q-btn>
    </div>


  </div>

</template>

<script>
import {reactive} from "vue";
import urls from "src/Urls";
import axios from "axios";
import {useQuasar} from "quasar";

export default {
  name: "ActivityCreatePage",
  data() {
    const $q = useQuasar()
    const address = new urls()
    const activity_info = reactive({
      name: '',
      category_list: [],
      properties: [],
      category_id: '',
      loading: true
    })


    function get_data() {
      axios.get(address.Category_list()).then(res => {
        if (res.status === 200) {
          activity_info.category_list.splice(0, activity_info.category_list.length)
          for (const item of res.data.item) {
            activity_info.category_list.push({
              name: item.name,
              id: item.id
            })
          }
          activity_info.loading = false

        }
      })
    }

    get_data()


    return {
      activity_info,
      address,
      get_data,
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
    Add() {
      this.activity_info.properties.push('')
    },
    del(index) {
      this.activity_info.properties.splice(index, 1)
    },
    save() {
      if (this.activity_info.name !== '' && this.activity_info.category_id !== '') {
        axios.post(this.address.activities_create(), {
          name: this.activity_info.name,
          properties: this.activity_info.properties,
          category_id: this.activity_info.category_id.id
        }).then(res => {
          if (res.data.Done) {
            this.toast(res.data.Message, 'green-9', 'white')
            this.activity_info.name =''
            this.activity_info.properties=[]
          }
          else {
            this.toast(res.data.Message, 'pink-6', 'white')
          }
        }).catch(()=>{
          this.toast('خطا در سرور', 'pink-6', 'white')
        })
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
  width: 90%;
  margin-right: 5%;
  margin-left: 5%;
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
</style>
