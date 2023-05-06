<template>
  <br>
  <div class="row" style="direction: rtl">
    <div class="col-md-12 col-xs-12">
      <q-table

        :columns="cols"
        :rows="rows"
        virtual-scroll
        flat bordered dense
        class="my-sticky-column-table full-width text"
        title="کالاهای مصرفی ایجاد شده"
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
                  <div class="col-md-2 q-pa-md">
                    <q-btn label="الحاق" class="full-width q-ma-md" dense color="indigo-10"
                           @click="Accession(props.key)"
                           text-color="white"></q-btn>
                  </div>
                  <div class="col-md-2 q-pa-md">
                    <q-btn label="حذف کردن الحاقی" class="full-width q-ma-md" dense color="grey-9"
                           @click="activated(props.key)"
                           text-color="white"></q-btn>
                  </div>
                  <div class="col-md-2 q-pa-md">
                    <q-btn label="اضافه کردن به انبار" class="full-width q-ma-md" dense color="purple-9"
                           @click="activated(props.key)"
                           text-color="white"></q-btn>
                  </div>
                  <div class="col-md-2 q-pa-md">
                    <q-btn label="اضافه کردن به خرابی ها" class="full-width q-ma-md" dense color="pink-6"
                           @click="activated(props.key)"
                           text-color="white"></q-btn>
                  </div>
                  <div class="col-md-2 q-pa-md">
                    <q-btn label="حذف کردن از انبار خرابی ها" class="full-width q-ma-md" dense color="teal-9"
                           @click="activated(props.key)"
                           text-color="white"></q-btn>
                  </div>

                  <div class="col-md-2 q-pa-md">
                    <q-btn label="مشاهده الحاق شده ها" class="full-width q-ma-md" dense color="light-blue-9"
                           disable
                           @click="activated(props.key)"
                           text-color="white"></q-btn>
                  </div>
                </div>

              </div>
            </q-td>
          </q-tr>
        </template>

      </q-table>
    </div>
  </div>


  <q-dialog v-model="dialogs.accession" full-width style="direction: rtl">
    <q-card>
      <q-card-section>
        <div class="text-h6 headers ">الحاقی</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="row">
          <div class="col-12">
            <q-input type="number"
                     dense
                     v-model="accession.serial"
                     maxlength="12" input-style="text-align: center"
                     label="شماره اموال"
                     class="inputs" standout label-color="black" color="green-9" outlined></q-input>
            <q-btn dense label="جستجو" @click="search_stock" class="q-ml-md q-mt-md inputs"></q-btn>
          </div>

        </div>
        <br>
        <div class="row">
          <div class="col-md-3 ">
            <label class="labels">نام محصول</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ accession.name }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">وضعیت</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ accession.active }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">نام مسئول</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ accession.response_name }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">نام دسته بندی</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ accession.category_name }}</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">نام واحد</label>
          </div>
          <div class="col-md-3 ">
            <label class="labels">{{ accession.position_name }}</label>
          </div>
          <div class="col-md-12">
            <div class="row" v-for="(item , index) in accession.properties">
              <div class="col-md-3 q-pa-xs">
                <label class="labels">{{ item }}</label>
              </div>
              <div class="col-md-3 q-pa-xs">
                <label class="labels">{{ accession.info[index] }}</label>
              </div>
            </div>
          </div>

        </div>
        <br>
        <div class="row" v-show="accession.searched">
          <div class="col-md-6">
            <q-input label="تعداد مورد الحاقی" type="number" class="inputs"
                     dense
                     v-model="accession.number"
                     maxlength="12" input-style="text-align: center"
                     standout label-color="black" color="green-9" outlined></q-input>
            <q-btn label="اضافه کردن" class="inputs q-mt-md" dense @click="Accession_add" color="indigo-10"></q-btn>
          </div>

        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="alert">
    <q-card>
      <q-card-section>
        <div class="text-h6">Alert</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro.
        Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="alert">
    <q-card>
      <q-card-section>
        <div class="text-h6">Alert</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro.
        Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="alert">
    <q-card>
      <q-card-section>
        <div class="text-h6">Alert</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro.
        Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>


  <q-dialog v-model="alert">
    <q-card>
      <q-card-section>
        <div class="text-h6">Alert</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro.
        Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

</template>

<script>
import {reactive} from "vue";
import {useQuasar} from "quasar";
import axios from "axios";
import urls from "src/Urls";

export default {
  name: "Form2Component",
  data() {
    const accession = reactive({
      stock_id: '',
      accession_id: '',
      name: '',
      active: '',
      category_name: '',
      category_id: '',
      response_name: '',
      position_name: '',
      info: [],
      properties: [],
      searched: false,
      number: 0,
      serial :''
    })
    const dialogs = reactive({
      accession: false,
      un_accession: false,
      add_stock: false,
      add_crash: false,
      delete_crash: false
    })
    const $q = useQuasar()
    const address = new urls()
    const cols = reactive([
      {name: 'name', required: true, label: 'نام محصول', align: 'center', field: 'name'},
      {name: 'serial', required: true, label: 'شماره سریال', align: 'center', field: 'serial'},
      {name: 'active', align: 'center', label: 'وضعیت', field: 'active'},
      {name: 'stock_number', align: 'center', label: 'تعداد در انبار', field: 'stock_number'},
      {name: 'crash', align: 'center', label: 'تعداد خرابی ها', field: 'crash'},
      {name: 'uses', align: 'center', label: 'تعداد درحال استفاده', field: 'uses'},
      {name: 'total', align: 'center', label: 'تعداد کل', field: 'total'},
    ])
    const rows = reactive([])

    function Loading_data() {
      rows.splice( 0  , rows.length)
      axios.get(address.Stock_consumer_list()).then(res => {
        for (const item of res.data.items) {
          rows.push({
            stock_number: item.stock_number,
            name: item.name,
            id: item.id,
            active: item.active,
            serial: item.serial,
            uses: item.use_number,
            crash: item.crash_number,
            total: item.total_number
          })
        }
      }).catch(() => {
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

    Loading_data()


    return {
      Loading_data,
      address,
      cols,
      rows,
      dialogs,
      accession,
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
    Accession(item) {
      this.dialogs.accession = true
      this.accession.stock_id = item
    },
    search_stock() {
      if (this.accession.serial !== '') {
        axios.get(this.address.stock_list_is_consumere(), {
          params: {
            text: this.accession.serial,
            is_consumer: false
          }
        }).then(res => {
          if (res.status === 200) {
            if (res.data.items.length > 0) {
              this.accession.accession_id = res.data.items[0].id
              this.accession.name = res.data.items[0].name
              this.accession.category_name = res.data.items[0].category_name
              this.accession.category_id = res.data.items[0].category_id
              this.accession.response_name = res.data.items[0].response_name
              this.accession.active = res.data.items[0].active
              this.accession.position_name = res.data.items[0].position_name
              this.accession.info = res.data.items[0].info
              this.accession.properties = res.data.items[0].properties
              this.toast('بروز رسانی با موفقیت انجام شد', 'green-9', 'white')
              this.accession.searched = true

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
        this.toast('خطای داخلی سرور', 'pink-6', 'white')
      }

    },
    Accession_add() {
      if (this.accession.serial > 0) {
        axios.put(this.address.stock_accession(), {
          "number": this.accession.number,
          "stock_id": this.accession.stock_id,
          "accession_number": this.accession.stock_id
        }).then(res => {
          if (res.data.Done) {

            this.accession.accession_id = ''
            this.accession.response_name = ''
            this.accession.category_name = ''
            this.accession.active = ''
            this.accession.name = ''
            this.dialogs.accession = false
            this.accession.stock_id = ''
            this.accession.position_name = ''
            this.accession.info = []
            this.accession.properties = []
            this.accession.searched = false
            this.accession.number = 0
            this.dialogs.accession = false
            this.Loading_data()
          } else {
            this.toast(res.data.Message, 'pink-6', 'white')
          }
        }).catch(() => {
          this.toast('خطای داخلی سرور', 'pink-6', 'white')
        })
      } else {
        this.toast('می بایست برای الحاق تعداد آن بیش از صقر باشد', 'pink-6', 'white')
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
</style>
