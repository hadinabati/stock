<template>
  <div class="row" style="direction: rtl">
    <div class="col-md-2"></div>
    <div class="col-md-8 col-xs-12 q-m-a-md">
      <div class="row">
        <div class="col-8">
          <div v-if="read_only">
            <q-input v-model="repair_info.stock_number" readonly :model-value="stock_number" type="number"
                     maxlength="12" input-style="text-align: center"
                     label="شماره اموال"
                     class="inputs q-pa-md" standout label-color="black" color="green-9" outlined></q-input>
          </div>
          <div v-else>
            <q-input v-model="repair_info.stock_number" type="number" maxlength="12" input-style="text-align: center"
                     label="شماره اموال"
                     class="inputs q-pa-md" standout label-color="black" color="green-9" outlined></q-input>
          </div>

        </div>
        <div class="col-4">
          <q-btn dense label="جستجو" @click="search_stock" class="full-width q-pa-md q-mt-md"></q-btn>
        </div>
      </div>
      <br>
      <hr style="border: 1px dotted #ea8282">
      <br>
      <div v-show="repair_info.searched">
        <div class="row">
          <div class="col-md-3 ">
            <label class="labels">نام محصول</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ repair_info.info.name }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">وضعیت</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ repair_info.info.active }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">نام مسئول</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ repair_info.info.response_name }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">نام دسته بندی</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ repair_info.info.category_name }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">نام واحد</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ repair_info.info.position_name }}</label>
          </div>
          <div class="col-md-12">
            <div class="row" v-for="(item , index) in repair_info.info.properties">
              <div class="col-md-3 q-pa-xs">
                <label class="labels">{{ item }}</label>
              </div>
              <div class="col-md-3 q-pa-xs">
                <label class="labels">{{ repair_info.info.info[index] }}</label>
              </div>
            </div>
          </div>

        </div>
        <div class="row">
          <div class="col-md-8 col-xs-12">
            <div class="row">
              <div class="full-width q-mt-lg q-mb-md">
                <label class="labels"> دسته بندی</label>
                <q-select
                  v-model="repair_info.activity_id"
                  :options="repair_info.activity_list"
                  option-value="id" option-label="name" dense color="green-9" outlined
                  square class="inputs" input-style="text-align: center ;">
                </q-select>


              </div>
              <div v-for="(item , index ) in repair_info.activity_id.properties" :key="index"
                   class="full-width q-mt-lg q-mb-md">
                <label class="labels">{{ item }}</label>
                <q-input
                  outlined
                  standout
                  v-model="repair_info.activity_properties[index]"
                  square class="inputs" input-style="text-align: center ;">
                </q-input>


              </div>
            </div>
            <div class="row">

              <div class="full-width q-mt-lg q-mb-md">
                <label class="labels">توضیحات</label>
                <q-input type="textarea" color="green-9" outlined
                         v-model="repair_info.description"
                         square class="inputs" input-style="text-align: center ;">
                </q-input>
              </div>


            </div>
            <div class="row">

              <div class="full-width q-mt-lg q-mb-md">
                <label class="labels">آیا نیاز به بروز رسانی داید ؟ </label>
                <q-radio disable checked-icon="task_alt" unchecked-icon="panorama_fish_eye" v-model="repair_info.is_updated"
                         name="check" label="بلی" :val="true" class="q-ma-xs inputs" dense>
                </q-radio>
                <q-radio checked-icon="task_alt" unchecked-icon="panorama_fish_eye" :val="false"
                         v-model="repair_info.is_updated" name="check" label="خیر" class="q-ma-xs inputs" dense>
                </q-radio>


              </div>
            </div>
          </div>
          <div class="col-md-8 q-mt-md">
            <UpdateStockComponent v-show="repair_info.is_updated"></UpdateStockComponent>
          </div>
        </div>
        <div class="row">
          <q-btn @click="save" label="ذخیره داده ها " class="full-width" color="deep-purple-14">
          </q-btn>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import {reactive} from "vue";
import UpdateStockComponent from "pages/UpdateStockComponent.vue";
import urls from "src/Urls";
import axios from "axios";
import {useQuasar} from "quasar";

export default {
  name: "Form1Component",
  components: {
    UpdateStockComponent
  },
  props: {
    stock_number: Int16Array,
    read_only: Boolean
  },
  data() {
    const $q = useQuasar()
    const address = new urls()
    const repair_info = reactive({
      info: {
        name: '',
        active: '',
        category_name: '',
        category_id: '',
        response_name: '',
        position_name: '',
        info: [],
        properties: []

      },
      searched: false,
      stock_number: '',
      is_updated: false,
      activity_list: [],
      activity_id: '',
      activity_properties: [],
      description: '',
      stock_id: ''

    })


    function Activity_list(category_id) {
      repair_info.activity_list.splice(0, repair_info.activity_list.length)
      axios.get(address.activities_list() + '/' + category_id).then(
        res => {
          if (res.status === 200) {
            if (res.data.data.length > 0) {
              for (const activity of res.data.data) {
                if (activity.active){
                  repair_info.activity_list.push({
                    name: activity.name,
                    id: activity.id,
                    properties: activity.properties
                  })
                }

              }
            } else {
              $q.notify({
                position: 'bottom',
                timeout: 1500,
                message: 'داده ای یافت نشد',
                color: 'pink-6',
                textColor: 'white',
                classes: 'notify_center',
              })

            }

          }
        }
      ).catch(() => {
        $q.notify({
          position: 'bottom',
          timeout: 1500,
          message: 'خطای داخلی سرور',
          color: 'pink-6',
          textColor: 'white',
          classes: 'notify_center',
        })
      })
    }


    return {
      Activity_list,
      repair_info,
      address,
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
    search_stock() {
      if (this.read_only) {
        this.repair_info.stock_number = this.stock_number
      }
      if (this.repair_info.stock_number !== '') {
        axios.get(this.address.stock_list_is_consumere(), {
          params: {
            text: this.repair_info.stock_number,
            is_consumer: false
          }
        }).then(res => {
          if (res.status === 200) {
            if (res.data.items.length > 0) {
              this.repair_info.stock_id = res.data.items[0].id
              this.repair_info.info.name = res.data.items[0].name
              this.repair_info.info.category_name = res.data.items[0].category_name
              this.repair_info.info.category_id = res.data.items[0].category_id
              this.repair_info.info.response_name = res.data.items[0].response_name
              this.repair_info.info.active = res.data.items[0].active
              this.repair_info.info.position_name = res.data.items[0].position_name
              this.repair_info.info.info = res.data.items[0].info
              this.repair_info.info.properties = res.data.items[0].properties
              this.repair_info.searched = true
              this.toast('بروز رسانی با موفقیت انجام شد', 'green-9', 'white')
              this.Activity_list(this.repair_info.info.category_id)
            } else {
              this.toast('داده ای یافت نشد', 'pink-6', 'white')

            }

          } else {
            this.toast('خطا در دریافت اطلاعات', 'pink-6', 'white')
          }
        }).catch(() => {
          this.toast('خطای داخلی سرور', 'pink-6', 'white')
        })
      } else {
        this.toast('لطفا شماره اموال را وارد نمایید', 'pink-6', 'white')
      }

    },
    save() {
      if (this.repair_info.is_updated) {
        alert('need updated')
      } else {
        axios.post(this.address.repair_create(), {
          "id_of_creator": '6432fde4de420c8131e423e2',
          "activity_id": this.repair_info.activity_id.id,
          "description": this.repair_info.description,
          "stock_updated": false,
          "properties": this.repair_info.activity_properties,
          "stock_id": this.repair_info.stock_id
        }).then(
          res => {
            if (res.data.Done) {
              this.repair_info.activity_id = ''
              this.repair_info.description = ''
              this.repair_info.activity_properties = []
              this.repair_info.stock_id = ''
              this.repair_info.stock_number = ''
              this.repair_info.searched = false
              this.toast(res.data.Message, 'green-9', 'white')
            } else {
              this.toast(res.data.Message, 'pink-6', 'white')
            }
          }
        ).catch(() => {
          this.toast('خطای داخلی سرور', 'pink-6', 'white')
        })
      }
    }
  }
}
</script>

<style scoped>
.inputs {
  font-family: iransans_r;
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
