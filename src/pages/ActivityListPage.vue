<template>
  <div class="row q-ma-lg">
    <div class="col-12">
      <p class="headers">لیست فعالیت های ایجاد شده</p>
    </div>
  </div>
  <div class="row q-mt-lg">
    <q-table
      :columns="columns"
      :rows="rows"
      virtual-scroll
      flat bordered dense
      class="my-sticky-column-table full-width text"
      title="فعالیت های ایجاد شده"
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
                  <q-btn label="فعالسازی" class="full-width q-ma-md" dense color="amber-10"
                         :disable="props.row.active"
                         @click="activated(props.key)"
                         text-color="white"></q-btn>
                </div>

                <div class="col-md-2 q-pa-xs ">
                  <q-btn :disable="!props.row.active" label="غیر فعالسازی" class="full-width q-ma-md" dense
                         color="pink-6"
                         @click="deactivate(props.key)"
                         text-color="white"></q-btn>
                </div>
              </div>
            </div>
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>
</template>

<script>
import axios from "axios";
import urls from "src/Urls";
import {reactive} from "vue";
import {useQuasar} from "quasar";

export default {
  name: "ActivityListPage",
  data() {
    const address = new urls()
    const columns = [
      {name: 'name', required: true, label: 'نام محصول', align: 'center', field: 'name'},
      {name: 'active', align: 'center', label: 'وضعیت', field: 'active'},
      {name: 'properties', align: 'center', label: 'ویژگی ها', field: 'properties'},
    ]
    const rows = reactive([])
    const $q = useQuasar()

    function LoadData() {
      axios.get(address.activities_list()).then(res => {
        if (res.status === 200) {
          rows.splice(0, rows.length)
          for (const item of res.data.data) {
            rows.push({
              id: item.id,
              name: item.name,
              properties: item.properties,
              active: item.active
            })

          }
        }
      })
    }

    LoadData()


    return {
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
      address,
      columns,
      LoadData,
      rows

    }
  },

  methods: {
    deactivate(id) {
      axios.delete(this.address.activities_delete(), {
        data: {
          id: id
        }
      }).then(res => {
        if (res.data.Done) {
          this.toast(res.data.Message, 'green-9', 'white')
          this.LoadData()
        } else {
          this.toast(res.data.Message, 'pink-6', 'white')
        }
      }).catch(() => {
        this.toast('خطا در سرور', 'pink-6', 'white')
      })

    },
    activated(id) {
      axios.put(this.address.activities_active(), {
        id: id
      }).then(res => {
        if (res.data.Done) {
          this.toast(res.data.Message, 'green-9', 'white')
          this.LoadData()
        } else {
          this.toast(res.data.Message, 'pink-6', 'white')
        }
      }).catch(() => {
        this.toast('خطا در سرور', 'pink-6', 'white')
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
