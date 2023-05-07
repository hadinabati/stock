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
                  <q-btn @click="repair_btn_list(props.key)" label="تاریخچه تعمیرات" class="full-width q-ma-md" dense color="indigo-10"
                         text-color="white"></q-btn>
                </div>
                <div class="col-md-2 q-pa-xs ">
                  <q-btn disable label="بروز رسانی" class="full-width q-ma-md" dense color="lime-10" text-color="dark"></q-btn>
                </div>
                <div class="col-md-2 q-pa-xs ">
                  <q-btn label=" لیست بروز رسانی ها" class="full-width q-ma-md" dense color="teal-9 "
                         text-color="white"></q-btn>
                </div>
                <div class="col-md-2 q-pa-xs ">
                  <q-btn label="مشخصات" class="full-width q-ma-md" dense color="cyan-9" text-color="white"></q-btn>
                </div>
              </div>
            </div>
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>


  <q-dialog  v-model="dialogs.repair_list_dialog" style="direction: rtl">
    <q-card>
      <q-card-section>
        <div class="text-h6 headers">تاریخچه تعمیرات </div>
      </q-card-section>

      <q-card-section class="q-pt-none">

        <div class="row text" v-for="(item , index) in repair_history" :key="index">
          <div class="col-2">
            {{index + 1}}
          </div>
          <div class="col-10">
            <div class="row">
              <div class="col-12">
                <label class="text">نام:
                  <span class="q-mr-md q-ml-md">
                {{item.name}}
              </span>

                </label>
              </div>
              <div class="col-12">
                <label class="text">توضیحات:
                  <span class="q-mr-md q-ml-md">
                  {{item.update_history.description}}
              </span>

                </label>
              </div>
              <div class="col-12">
                <label class="text">تاریخ تعویض:
                  <span class="q-mr-md q-ml-md">
                  {{item.update_at}}
              </span>

                </label>
              </div>
              <div  class="col-12">
                <div v-for="(sub , sub_index) in item.update_history.properties" :key="sub_index">
                  {{sub}} : {{item.activity_properties[sub_index]}}

                </div>
              </div>
              <div class="col-12">
                <hr>
              </div>
            </div>
          </div>

        </div>



      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>




</template>

<script>
import {reactive, ref} from "vue";
import urls from "src/Urls";
import axios from "axios";
import {useQuasar} from "quasar";

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

    const   repair_history = reactive([
      {
        name : '',
        update_history :{
          description :'',
          properties:'',
          activity_id:''
        },
        activity_properties:[],
        update_at :''

      }
    ])



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
        }
        else {
          Message('اطلاعاتی یافت نشد', 'pink-6', 'white')
        }

      }).catch(res => {
        Message('خطا در دریافت اطلاعات', 'pink-6', 'white')
      })
    }

    Loading_data()

    return {
      repair_history,
      search_text,
      Message,
      columns,
      data_list,
      searched_list,
      searched,
      dialogs

    }
  },

  methods: {
    search() {
      if (this.search_text !== '') {
        this.searched = true
        const address = new urls()
        axios.get(address.stock_list_single() , {
          params:{
            text:this.search_text
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
      }
      else {
        this.searched = false
      }

    } ,

    repair_btn_list(id){
      const  address= new urls()
      axios.get(address.stock_repair_id() +'/' + id).then(res =>{
        if (res.status ===200){
          if (res.data.data.length>0){
            this.repair_history.splice( 0 , this.repair_history.length)
            for (const item of res.data.data) {
              const day = new Date(item.update_at.toString());
                  this.repair_history.push({
                    name : item.name,
                    update_history :item.update_history,
                    activity_properties:item.activity_properties,
                    update_at : new persianDate(day).format('LLLL')
                  })

              this.dialogs.repair_list_dialog = true
            }

          }
          else {
            this.Message(" اطلاعاتی برای این کالا در تعمیرات به ثبت نرسیده است","amber-10","white")
          }
        }
        else {
          this.Message("خطا در دریافت اطلاعات ","pink-6","white")
        }
      }).catch(()=>{
        this.Message("خطای داخلی سرور","pink-6","white")
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
