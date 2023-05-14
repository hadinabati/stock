<template>
  <div class="row">
    <p class="headers q-pa-md"> بروز رسانی کالا </p>
    <div class="col-md-12 col-xs-12">
      <div class="col-md-4 q-pa-md">
        <div class="full-width q-mt-lg">
          <label class="labels"> نام کالا </label>
          <q-input v-model="stock_data.name" type="text" input-style="text-align: center"
                   class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
        </div>
      </div>
      <div class="col-md-4 q-pa-md">
        <div class="full-width q-mt-lg">
          <label class="labels"> شماره اموال </label>
          <q-input v-model="stock_data.stock_number" type="number" maxlength="100" input-style="text-align: center"
                   class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
        </div>
      </div>


    </div>
    <div class="col-md-12 col-xs-12">
      <div class="col-md-4 q-pa-md">
        <div class="full-width q-mt-lg">
          <label class="labels">مسلول </label>
          <q-select @update:model-value="check" v-model="stock_data.has_response" :options="response"
                    option-value="id" option-label="label" dense color="green-9" outlined
                    square class="inputs" input-style="text-align: center ;">
          </q-select>
        </div>
      </div>
      <div class="col-md-4 q-pa-md">
        <template v-if="!stock_data.has_response_id">
          <div class="full-width q-mt-lg">
            <q-input label="جستجو" outlined dense v-model="stock_data.filter_name" @update:model-value="filter_name"
                     class="inputs q-mb-xs"></q-input>
            <template v-if="stock_data.searched_name">
              <q-select
                option-value="id"
                option-label="name"
                v-model="stock_data.response_id"
                :options="stock_data.searched_list_name"
                dense
                color="green-9"
                outlined
                square class="inputs"
                input-style="text-align: center ;"
              >
              </q-select>
            </template>
            <template v-else>
              <q-select
                option-value="id"
                option-label="name"
                v-model="stock_data.response_id"
                :options="lists.person_list"
                dense
                color="green-9"
                outlined
                square class="inputs"
                input-style="text-align: center ;"
              >
              </q-select>
            </template>


          </div>
        </template>
        <template v-else>
          <div class="full-width q-mt-lg">
            <label class="labels">نام قسمت </label>
            <q-select :options="lists.position_list" option-value="id" option-label="name"
                      v-model="stock_data.position_id" dense color="green-9" outlined
                      square class="inputs" input-style="text-align: center ;">
            </q-select>
          </div>
        </template>

      </div>
      <div class="col-md-4 q-pa-md">
        <div class="full-width q-mt-lg">
          <label class="labels">دسته بندی </label>
        </div>
        <div class="row">
          <template v-for="(item , index) in properties" :key="index">
            <div class="col-md-6 q-pa-md">
              <q-input readonly input-style="text-align: center"
                       class="inputs" square rounded label-color="black" color="green-9" :model-value="item" outlined
                       dense></q-input>
            </div>
            <div class="col-md-6 q-pa-md">
              <q-input v-model="stock_data.category_info_filled[index]" input-style="text-align: center"
                       class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
            </div>
          </template>
        </div>
      </div>
      <div class="col-md-4 q-pa-md">
        <template v-if="is_consumer">
          <div class="full-width q-mt-lg">
            <label class="labels">تعداد واحد </label>
            <q-input v-model="stock_data.count" type="number" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </template>
        <template v-else>
          <div class="full-width q-mt-lg">
            <label class="labels">تعداد واحد </label>
            <q-input readonly type="text" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense
                     model-value="یک واحد"></q-input>
          </div>
        </template>
      </div>
    </div>
    <div class="col-md-1"></div>
    <div class="col-md-10  col-xs-12">
      <q-btn label="ثبت نهایی" color="indigo-10" class="full-width" @click="save"></q-btn>
    </div>
  </div>

</template>


<script>
import {reactive} from "vue";
import urls from "src/Urls";
import axios from "axios";
import {useQuasar} from "quasar";

export default {
  name: "UpdateStockComponent",
  props: {
    properties: [],
    cat_id: '',
    id: '',
    old_stock_number: '',
    is_consumer: ''
  },
  data() {
    const stock_data = reactive({
      searched_name: false,
      searched_list_name: [],
      filter_name: '',
      name: '',
      stock_number: '',
      is_consumer: '',
      has_response: '',
      has_response_id: false,
      number: '',
      info: [],
      response_id: '',
      position_id: '',
      category_id: [],
      count: 1,
      category_info_filled: []
    })
    const lists = reactive({
      category_list: [],
      position_list: [],
      person_list: [],
      category_options_selected: []

    })
    const address = new urls()
    const kind = reactive([
      {
        label: 'مصرفی می باشد',
        id: true
      },
      {
        label: 'غیر مصرفی',
        id: false
      }
    ])
    const response = reactive([
      {
        label: 'دارای شخص واحدی به عنوان مسئول می باشد',
        id: true
      },
      {
        label: 'شخصی مسئول این کالا نیست',
        id: false
      }
    ])
    const $q = useQuasar()

    function get_data() {
      axios.get(address.person_list()).then(res => {
        if (res.data.Done) {
          lists.person_list.splice(0, lists.person_list.length)
          for (let i = 0; i < res.data.data.length; i++) {
            lists.person_list.push({
              "name": res.data.data[i].name + '  -  ' + res.data.data[i].family,
              "id": res.data.data[i].id
            })

          }
        }

      })
      axios.get(address.position_list()).then(res => {
        if (res.status === 200) {
          lists.position_list.splice(0, lists.position_list.length)
          for (let i = 0; i < res.data.item.length; i++) {
            lists.position_list.push({
              "name": res.data.item[i].name,
              "description": res.data.item[i].description,
              "id": res.data.item[i].id
            })

          }

        }
      })
    }

    get_data()


    return {
      get_data,
      address,
      kind,
      stock_data,
      response,
      lists,
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
    check() {
      if (this.stock_data.has_response.id) {
        this.stock_data.has_response_id = true

      } else {
        this.stock_data.has_response_id = false
      }
    },
    save() {
      const info = []
      for (const info_item of this.stock_data.category_info_filled) {
        info.push(info_item)
      }
      const stock_info = {
        id: this.id,
        name: this.stock_data.name,
        is_consumer: this.is_consumer,
        has_response: true,
        category_id: this.cat_id,
        response_id: this.stock_data.response_id.id,
        position_id: this.stock_data.position_id.id,
        stock_number: parseInt(this.stock_data.stock_number),
        info: info,
        count: this.stock_data.count,
        old_stock: this.old_stock_number,
        active: true
      }
      if (this.stock_data.position_id.id === undefined) {
        stock_info.position_id = ''
      }
      if (this.stock_data.response_id.id === undefined) {
        stock_info.response_id = ''
        stock_info.has_response = false
      }

      this.$emit('child_data_update_stock', stock_info)


    },
    filter_name() {
      if (this.stock_data.filter_name !== '') {
        this.stock_data.searched_name = true
        this.stock_data.searched_list_name.splice(0, this.stock_data.searched_list_name.length)
        for (let i = 0; i < this.lists.person_list.length; i++) {
          if (this.lists.person_list[i].name.includes(this.stock_data.filter_name)) {
            this.stock_data.searched_list_name.push({
              "name": this.lists.person_list[i].name,
              "id": this.lists.person_list[i].id
            })

          }
        }
      } else {
        this.stock_data.searched_name = false
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
