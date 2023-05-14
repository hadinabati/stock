<template>
  <div class="row q-pa-md">
    <p class="headers"> لیست کالا های ثبت شده</p>
    <div class="col-md-12">
      <div class="row">
        <div class="col-md-4 q-pa-md">
          <q-input dense class="inputs" v-model="search_text" label="جستجو" standout></q-input>
        </div>
        <div class="col-md-2 q-pa-md">
          <q-btn dense label="جستجو" @click="search" class="full-width " color="indigo-10"></q-btn>
        </div>
      </div>

    </div>
  </div>
  <div class="q-ma-md">
    <q-table
      virtual-scroll
      flat bordered dense
      class="my-sticky-column-table text"
      title="کالاهای ثبت شده"
      :rows="searched ? searched_list : data_list"
      :columns="columns"
      row-key="id"

    >

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width/>
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="sm" color="accent" round dense @click="props.expand = !props.expand"
                   :icon="props.expand ? 'remove' : 'add'"/>
          </q-td>
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">
              <div class="row">
                <div class="col-md-2 q-pa-xs ">
                  <q-btn v-show="!props.row.consumer" @click="repair_btn_list(props.key)" label="تاریخچه تعمیرات"
                         class="full-width q-ma-md" dense
                         color="indigo-10"
                         text-color="white"></q-btn>
                </div>
                <div class="col-md-2 q-pa-xs ">
                  <q-btn v-show="!props.row.consumer"
                         @click="update_dialog(props.key ,props.row.is_consumer ,  props.row.stock_number , props.row.category_id , props.row.properties)"
                         label="بروز رسانی" class="full-width q-ma-md" dense
                         color="deep-orange-6"
                         text-color="white"></q-btn>
                </div>
                <div v-show="!props.row.consumer" class="col-md-2 q-pa-xs ">
                  <q-btn label=" لیست بروز رسانی ها" class="full-width q-ma-md" dense color="teal-9 "
                         text-color="white" @click="show_updated(props.row.update_history , props.row.name)"></q-btn>
                </div>
                <div class="col-md-2 q-pa-xs ">
                  <q-btn v-show="!props.row.consumer" label="مشخصات" @click="show_info(props.row.stock_number)" class="full-width q-ma-md" dense
                         color="cyan-9" text-color="white"></q-btn>
                </div>
              </div>
            </div>
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>


  <q-dialog v-model="dialogs.repair_list_dialog" style="direction: rtl">
    <q-card>
      <q-card-section>
        <div class="text-h6 headers">تاریخچه تعمیرات</div>
      </q-card-section>

      <q-card-section class="q-pt-none">

        <div class="row text" v-for="(item , index) in repair_history " :key="index">
          <div class="col-2" style="margin-top: auto ; margin-bottom: auto">
            {{ index + 1 }}
          </div>
          <div class="col-10">
            <div class="row">
              <div class="col-12">
                <label class="text">نام:
                  <span class="q-mr-md q-ml-md">
                {{ item.name }}
              </span>

                </label>
              </div>
              <div class="col-12">
                <label class="text">توضیحات:
                  <span class="q-mr-md q-ml-md">
                  {{ item.description }}
              </span>

                </label>
              </div>
              <div class="col-12">
                <label class="text">تاریخ تعویض:
                  <span class="q-mr-md q-ml-md">
                  {{ item.update_at }}
              </span>

                </label>
              </div>

              <div class="col-12">
                <hr>
              </div>
            </div>
          </div>

        </div>


      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="dialogs.update_dialog" style="direction: rtl">
    <q-card>
      <q-card-section class="q-pt-none">
        <UpdateStockComponent @child_data_update_stock="save_update($event)" :id="stock_id"
                              :old_stock_number="stock_number" :is_consumer="is_consumer"
                              :cat_id="this.category_id" :properties="cat_properties"></UpdateStockComponent>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="خروج" color="pink-6" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="dialogs.update_list_dialog" style="direction: rtl">
    <q-card>
      <q-card-section>
        <div class="text-h6 headers">تاریخچه بروزرسانی ها</div>
      </q-card-section>

      <q-card-section class="q-pt-none">

        <div class="row text" v-for="(item , index) in update_history" :key="index">
          <div class="col-2" style="margin-top: auto ; margin-bottom: auto">
            {{ index + 1 }}
          </div>
          <div class="col-10">
            <div class="row">
              <div class="col-12">
                <label class="text">نام:
                  <span class="q-mr-md q-ml-md">
                {{ item.name }}
              </span>

                </label>
              </div>
              <div class="col-12">
                <label class="text">توضیحات:
                  <span class="q-mr-md q-ml-md">
                  {{ item.description }}
              </span>

                </label>
              </div>
              <div class="col-12">
                <label class="text">تاریخ تعویض:
                  <span class="q-mr-md q-ml-md">
                  {{ item.updated_at }}
              </span>

                </label>
              </div>

              <div class="col-12">
                <hr>
              </div>
            </div>
          </div>

        </div>


      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="dialogs.info_dialog" style="direction: rtl">
    <q-card>
      <q-card-section>
        <div class="text-h6 headers">مشخصات محصول</div>
      </q-card-section>

      <q-card-section class="q-pt-none">

        <div class="row text">
          <div class="col-4" style="margin-top: auto ; margin-bottom: auto">
            {{ info_history.stock_number }}
          </div>
          <div class="col-8">
            <div class="row">
              <div class="col-12">
                <label class="text">نام:
                  <span class="q-mr-md q-ml-md">
                {{ info_history.name }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">مسیول کالا:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.response_name }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">واحد کالا:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.position_name }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">این کالا به کسی ارجاع داده شده است:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.has_response }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">تعداد بروزرسانی ها:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.number_of_updated }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">تعداد تعمیرات:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.number_repair_history }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text"> تعداد کالا:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.count }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">وضعیت کالا:
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.active }}
              </span>

                </label>
              </div>
              <div class="col-12" style="border-top: 1px solid gray">
                <label class="text">تاریخ ثبت اولیه کالا :
                  <span class="q-mr-md q-ml-md">
                  {{ info_history.create_date }}
              </span>

                </label>
              </div>
              <br>
              <br>

              <br>
              <div class="col-12" v-for="(item , index) in info_history.info" :key="index" style="border-top: 1px solid gray">
                <label class="text">{{ item }} :<span class="q-mr-md q-ml-md">
                  {{ info_history.properties[index] }}
              </span>
                </label>
                <br>

              </div>
            </div>
          </div>

        </div>


      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

</template>

<script>
import {reactive, ref} from "vue";
import urls from "src/Urls";
import axios from "axios";
import {useQuasar} from "quasar";
import UpdateStockComponent from "pages/UpdateStockComponent.vue";

export default {
  name: "ProductPage",
  data() {
    const columns = [
      {name: 'name', required: true, label: 'نام محصول', align: 'center', field: 'name'},
      {name: 'stock_number', align: 'center', label: 'شماره اموال', field: 'stock_number'},
      {name: 'is_consumer', align: 'center', label: 'نوع کالا', field: 'is_consumer'},
      {name: 'create_date', align: 'center', label: 'تاریخ ایجاد', field: 'create_date'},
      {name: 'category_name', align: 'center', label: 'نام دسته', field: 'category_name'},
      {name: 'response_name', align: 'center', label: 'نام مسئول', field: 'response_name'},
      {name: 'active', align: 'center', label: 'وضعیت', field: 'active'},
      {name: 'position_name', align: 'center', label: 'نام واحد', field: 'position_name'},
      {name: 'count', align: 'center', label: 'تعداد', field: 'count'},

    ]
    const data_list = reactive([
      {
        id: '',
        name: '',
        stock_number: '',
        create_date: '',
        category_name: '',
        response_name: '',
        active: "",
        position_name: '',
        count: '',
        is_consumer: '',
        repair_history: [],
        update_history: [],
        info: [],
        properties: []
      }
    ])
    const searched_list = reactive([{
      id: '',
      name: '',
      stock_number: '',
      create_date: '',
      category_name: '',
      response_name: '',
      active: "",
      position_name: '',
      count: '',
      is_consumer: '',
      repair_history: [],
      update_history: [],
      info: [],
      properties: []
    }])
    const searched = ref(false)
    const dialogs = reactive({
      update_dialog: false,
      info_dialog: false,
      update_list_dialog: false,
      repair_dialog: false,
      repair_list_dialog: false,
    })
    const search_text = ref('')
    const $q = useQuasar()
    const repair_history = reactive([
      {
        name: '',
        description: '',
        update_at: ''

      }
    ])
    const stock_id = ref('')
    const is_consumer = ref(undefined)
    const stock_number = ref('')
    const category_id = ref('')
    const cat_properties = ref([])
    const update_history = [{
      name: '',
      description: '',
      updated_at: ''
    }]
    const info_history = reactive({
      name: '',
      position_name: '',
      response_name: '',
      has_response: '',
      number_of_updated: '',
      properties: [],
      info: [],
      count: '',
      number_repair_history: '',
      active: '',
      stock_number: '',
      create_date: ''

    })

    function Message(text, color, textColor) {
      const toast = $q.notify({
        position: 'bottom',
        timeout: 1500,
        message: text,
        color: color,
        textColor: textColor,
        classes: 'notify_center',
      })
      return toast


    }

    function Loading_data() {
      Message('درحال دریافت اطلاعات', 'amber-10', 'white')
      const address = new urls()

      axios.get(address.stock_list()).then(res => {
        if (res.status === 200) {
          data_list.splice(0, data_list.length)
          for (let i = 0; i < res.data.items.length; i++) {
            let result = res.data.items[i]
            let is_consumer = 'غیر مصرفی'
            let has_response = 'دارد'
            let active = 'فعال'
            let response_name = result.response_name
            const date = result.create_date
            const persin_date = new persianDate(date).format('LLLL')

            if (result.is_consumer) {
              is_consumer = ' مصرفی'
            }
            if (!result.has_response) {
              has_response = 'ندارد'
              response_name = 'ادمین اصلی'

            }
            if (!result.active) {
              active = 'غیر فعال'
            }


            data_list.push({
              category_id: result.category_id,
              consumer: result.is_consumer,
              id: result.id,
              name: result.name,
              stock_number: result.stock_number,
              create_date: persin_date,
              category_name: result.category_name,
              response_name: response_name,
              active: active,
              position_name: result.position_name,
              count: result.count,
              is_consumer: is_consumer,
              repair_history: result.repair_history,
              update_history: result.update_history,
              info: result.info,
              properties: result.properties
            })
          }
          Message('اطلاعات با موفقیت دریافت شدند', 'green-9', 'white')
        } else {
          Message('اطلاعاتی یافت نشد', 'pink-6', 'white')
        }

      }).catch(res => {
        Message('خطا در دریافت اطلاعات', 'pink-6', 'white')
      })
    }

    Loading_data()

    return {
      info_history,
      update_history,
      cat_properties,
      category_id,
      Loading_data,
      is_consumer,
      stock_number,
      stock_id,
      repair_history,
      search_text,
      Message,
      columns,
      data_list,
      searched_list,
      searched,
      dialogs,
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
  components: {
    UpdateStockComponent
  },
  methods: {
    search() {
      if (this.search_text !== '') {
        this.searched = true
        const address = new urls()
        axios.get(address.stock_list_single(), {
          params: {
            text: this.search_text
          }
        }).then(res => {
          if (res.status === 200) {
            this.searched_list.splice(0, this.searched_list.length)
            for (let i = 0; i < res.data.items.length; i++) {

              let result = res.data.items[i]

              let is_consumer = 'غیر مصرفی'
              let has_response = 'دارد'
              let active = 'فعال'
              let response_name = result.response_name
              const date = result.create_date
              const persin_date = new persianDate(date).format('LLLL')

              if (result.is_consumer) {
                is_consumer = ' مصرفی'
              }
              if (!result.has_response) {
                has_response = 'ندارد'
                response_name = 'ادمین اصلی'

              }
              if (!result.active) {
                active = 'غیر فعال'
              }

              this.searched_list.push({
                id: result.id,
                name: result.name,
                stock_number: result.stock_number,
                create_date: persin_date,
                category_name: result.category_name,
                response_name: response_name,
                active: active,
                position_name: result.position_name,
                count: result.count,
                is_consumer: is_consumer,
                repair_history: result.repair_history,
                update_history: result.update_history,
                info: result.info,
                properties: result.properties
              })
            }
            this.Message('اطلاعات با موفقیت دریافت شدند', 'green-9', 'white')
          } else {
            this.Message('اطلاعاتی یافت نشد', 'pink-6', 'white')
          }
        }).catch(() => {
          this.Message('خطا در دریافت اطلاعات', 'pink-6', 'white')
        })
      } else {
        this.searched = false
      }

    },
    repair_btn_list(id) {
      const address = new urls()
      axios.get(address.stock_repair_id() + '/' + id).then(res => {
        if (res.status === 200) {
          if (res.data.data.length > 0) {
            this.repair_history.splice(0, this.repair_history.length)
            for (const item of res.data.data) {
              const day = new Date(item.update_at);
              this.repair_history.push({
                name: item.name,
                description: item.description,
                update_at: new persianDate(day).format('LLLL')
              })

              this.dialogs.repair_list_dialog = true
            }

          } else {
            this.Message(" اطلاعاتی برای این کالا در تعمیرات به ثبت نرسیده است", "amber-10", "white")
          }
        } else {
          this.Message("خطا در دریافت اطلاعات ", "pink-6", "white")
        }
      }).catch(() => {
        this.Message("خطای داخلی سرور", "pink-6", "white")
      })
    },
    update_dialog(id, is_consumer, stock_number, category_id, properties) {
      this.stock_id = id
      this.stock_number = stock_number
      this.is_consumer = true
      this.category_id = category_id
      this.cat_properties = properties
      if (is_consumer == 'غیر مصرفی') {
        this.is_consumer = false
      }
      this.dialogs.update_dialog = true
    },
    save_update(item) {
      const address = new urls()
      axios.put(address.stock_update(), item).then(res => {
        if (res.data.Done) {
          this.toast('ثبت کالا با موفقیت انجام شد', 'green-9', 'white')
          this.dialogs.update_dialog = false
          this.Loading_data()
        } else {
          this.toast(res.data.Message, 'pink-6', 'white')
        }
      }).catch(() => {
        this.toast('خطای داخلی سرور', 'pink-6', 'white')
      })
    },
    show_updated(item, name) {
      this.update_history.splice(0, this.update_history.length)
      for (const updated of item) {
        const time = new Date(updated.updated_at)
        this.update_history.push({
          name: name,
          updated_at: new persianDate(time).format('LLLL'),
          description: updated.description
        })
      }

      this.dialogs.update_list_dialog = true
    },
    show_info(stock_number) {
      const address = new urls()
      axios.get(address.stock_list_is_consumere(), {
        params: {
          text: stock_number,
          is_consumer: false
        }
      }).then(res => {
        if (res.status === 200) {

          let active = 'فعال'
          const  date = new Date(res.data.items[0].create_date)
          if (!res.data.items[0].active) {
            active = 'غیر فعال'
          }
          let  has_response = 'بله'
          if (!res.data.items[0].has_response){
            has_response = 'خیر'
          }

          this.info_history.info = res.data.items[0].info
          this.info_history.name = res.data.items[0].name
          this.info_history.stock_number = res.data.items[0].stock_number
          this.info_history.count = res.data.items[0].count
          this.info_history.active = active
          this.info_history.create_date = new persianDate(date).format('LLLL'),
          this.info_history.number_repair_history = res.data.items[0].repair_history.length
          this.info_history.number_of_updated = res.data.items[0].update_history.length
          this.info_history.properties = res.data.items[0].properties
          this.info_history.response_name = res.data.items[0].response_name
          this.info_history.position_name = res.data.items[0].position_name
          this.info_history.has_response = has_response
          this.dialogs.info_dialog = true
        } else {
          this.toast('خطا در دریافت اطلاعات', 'pink-6', 'white')
        }
      }).catch(() => {
        this.toast('خطای سرور', 'pink-6', 'white')
      })
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


</style>
