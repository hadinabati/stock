<template>
  <h5 class="headers">ثبت و تغییرات قسمت های مربوطه</h5>
  <hr style="width: 50%">
  <div class="row q-mt-lg">
    <div class="col-md-6" style="border-left: 1px dashed black ; height: 80vh">
      <p class="text">ثبت واحد</p>
      <div class="full-width q-mt-lg">
        <label class="labels">نام واحد</label>
        <q-input input-style="text-align: center" v-model="Position.name" class="inputs" square rounded
                 label-color="black" color="green-9" outlined dense></q-input>
      </div>
      <div class="full-width q-mt-lg">
        <label class="labels">توضیحات</label>
        <q-input type="textarea" maxlength="100" v-model="Position.description" input-style="text-align: center"
                 class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
      </div>
      <div class="full-width q-mt-lg">
        <q-btn class="inputs" color="indigo-10" @click="save" label="ثبت واحد"></q-btn>
      </div>


    </div>
    <div class="col-md-6" style="border-right: 1px dashed black">
      <p class="text">واحد های ثبت شده</p>
      <div class="full-width q-mt-md q-pa-md">
        <table class="q-table q-table--bordered q-table--dense q-table--grid q-table--flat" style="font-size: 10pt">
          <thead>
          <tr>
            <td style="width: 12.5%">ردیف</td>
            <td style="width: 25%">نام واحد</td>
            <td style="width: 50%">توضیحات</td>
            <td style="width: 12.5%">ویرایش</td>
          </tr>
          </thead>
          <tbody>
          <tr v-for="( item, index) in DataPosition" :key="index">
            <td style="width: 12.5%">{{ index + 1 }}</td>
            <td style="width: 25%">{{ item.name }}</td>
            <td style="width: 50%">{{ item.description }}</td>
            <td style="width: 12.5%">
              <q-btn class="full-width q-pa-xs" @click="edit(item.id , index)" label="ویرایش" color="warning"
                     text-color="dark"></q-btn>
            </td>
          </tr>
          </tbody>
        </table>
      </div>


    </div>
  </div>

  <q-dialog
    style="direction: rtl"
    v-model="alart"
    full-width

  >
    <q-card style="width: 600px">
      <q-card-section>
        <div class="text-h6 headers ">تغییرات</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="full-width q-mt-lg">
          <label class="labels">{{ 'نام مربوط  به ' + '   -   ' + Update.old_name }}</label>
          <q-input input-style="text-align: center" v-model="Update.new_name" class="inputs" square rounded
                   label-color="black" color="green-9" outlined dense></q-input>
        </div>
        <div class="full-width q-mt-lg">
          <label class="labels"> {{ 'توضیخات مربوط به ' + '    -   ' + Update.old_description }}</label>
          <q-input type="textarea" maxlength="100" v-model="Update.new_description" input-style="text-align: center"
                   class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
        </div>
        <div class="full-width q-mt-lg">
          <q-btn class="inputs" color="indigo-10" @click="updated" label="ثبت واحد"></q-btn>
        </div>
      </q-card-section>

      <q-card-actions align="left" class="bg-white text-pink-6">
        <q-btn flat label="خروج" v-close-popup class="text"/>
      </q-card-actions>
    </q-card>
  </q-dialog>

</template>

<script>
import {reactive, ref} from "vue";
import axios from "axios";
import urls from "src/Urls";
import {useQuasar} from "quasar";

export default {
  name: "PositionPage",

  data() {
    const DataPosition = reactive([])
    const Position = reactive({
      name: '',
      description: ''
    })
    const Update = reactive({
      old_name: '',
      new_name: '',
      old_description: '',
      new_description: '',
      id: ''
    })
    const $q = useQuasar()
    const alart = ref(false)

    function start() {
      const address = new urls()
      axios.get(address.position_list()).then(response => {
        if (response.status === 200) {
          DataPosition.splice(0, DataPosition.length)
          for (let i = 0; i < response.data.item.length; i++) {
            DataPosition.push({
              name: response.data.item[i].name,
              description: response.data.item[i].description,
              id: response.data.item[i].id,
            })
          }
        }
      })
    }

    start()

    return {
      Update,
      alart,
      start,
      DataPosition,
      Position,
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
    save() {
      if (this.Position.name !== '' && this.Position.description !== '') {
        const address = new urls()
        axios.post(address.position_create(), {
          name: this.Position.name,
          description: this.Position.description
        }).then(response => {
          if (response.data.Done) {
            this.toast(response.data.Message, 'indigo-10', 'white')
            this.start()
            this.Position.name = ''
            this.Position.description = ''
          } else {
            this.toast(response.data.Message, 'pink-8', 'white')
          }
        })
      } else {
        this.toast('لطفا فیلد ها را کامل نمایید', 'pink-8', 'white')

      }

    },
    edit(id, index) {
      this.Update.id = id
      this.Update.old_name = this.DataPosition[index].name
      this.Update.old_description = this.DataPosition[index].description
      this.alart = true
    },
    updated() {
      if (this.Update.new_name !== '' && this.Update.new_description !== '') {
        const address = new urls()
        axios.put(address.position_update(), {
          name: this.Update.new_name,
          description: this.Update.new_description,
          id: this.Update.id
        }).then(response => {
          if (response.data.Done) {
            this.toast(response.data.Message, 'indigo-10', 'white')
            this.start()
            this.Update.new_name = ''
            this.Update.new_description = ''
            this.Update.id = ''
            this.Update.old_name = ''
            this.Update.old_description = ''
            this.alart = false
          } else {
            this.toast(response.data.Message, 'pink-8', 'white')
          }
        })
      } else {
        this.toast('لطفا فیلد ها را کامل نمایید', 'pink-8', 'white')

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
  font-size: 11pt;
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
