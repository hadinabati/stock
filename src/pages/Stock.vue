<template>
  <div class="row">
    <div class="col-md-12">
      <p class="headers q-mt-lg">ثبت دسته بندی کالا های انبار</p>
    </div>


  </div>
  <div class="row">
    <div class="col-md-6">
      <div class="row">
        <div class="col-md-12">
          <div class="full-width q-mt-lg">
            <label class="labels"> نام دسته بندی </label>
            <q-input type="text" maxlength="100" input-style="text-align: center" v-model="info_data.name"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>
        <div class="col-md-12">
          <div class="full-width q-mt-lg">
            <label class="labels"> توضیحات </label>
            <q-input type="textarea" maxlength="100" input-style="text-align: center" v-model="info_data.description"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>
        <div class="col-md-12" style="border-bottom: 1px dotted #928e9c">
          <div class="full-width q-mt-lg q-mb-md">
            <q-btn @click="AddRow" label="اضافه کردن توضیحات" class="inputs"
                   style="width: 60% ; margin-left: 20% ; margin-right: 20%"
                   rounded label-color="white" color="light-blue-10" outlined dense></q-btn>
          </div>

        </div>
        <div class="col-md-12">
          <div style="border-bottom: #928e9c 1px dotted" class="row q-pb-md">
            <template v-for="(item  , index) in info_list" :key="index">
              <div class="col-md-8 ">
                <label class="labels"> توضیحات </label>
                <q-input type="text" maxlength="100" input-style="text-align: center" v-model="info_list[index].name"
                         class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
              </div>
              <div class="col-md-4">
                <label class="labels"> </label>
                <q-btn @click='DeleteRow(index)' label="حذف کردن" class="inputs"
                       style="width: 60% ; margin-left: 20% ; margin-right: 20%"
                       rounded label-color="white" color="pink-6" outlined dense></q-btn>
              </div>
            </template>

          </div>
        </div>
        <div class="full-width q-mt-lg">
          <q-btn class="inputs" color="indigo-10" @click="save" label="ثبت دسته بندی"></q-btn>
        </div>
      </div>

    </div>
    <div class="col-md-6" style="border-right: 1px dashed black">
      <p class="text">واحد های ثبت شده</p>
      <div class="full-width q-mt-md q-pa-md">
        <table class="q-table q-table--bordered q-table--dense q-table--grid q-table--flat" style="font-size: 10pt">
          <thead>
          <tr>
            <td style="width: 12.5%">ردیف</td>
            <td style="width: 20%">نام واحد</td>
            <td style="width: 25%">توضیحات</td>
            <td style="width: 30%">مشخصات</td>
            <td style="width: 12.5%">ویرایش</td>
          </tr>
          </thead>
          <tbody>
          <tr v-for="( item, index) in CategoryList" :key="index">
            <td style="width: 12.5%">{{ index + 1 }}</td>
            <td style="width: 20%">{{ item.name }}</td>
            <td style="width: 25%">{{ item.description }}</td>
            <td style="width: 30%">
              <template v-for="row in item.info" :key="row">
                <label class="q-pa-xs">{{ row }} - </label>
              </template>
            </td>
            <td style="width: 12.5%">
              <q-btn class="full-width q-pa-xs" @click="Edit(item.id , index)" label="ویرایش" color="warning"
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
    v-model="dialog"
    full-width

  >
    <q-card style="width: 600px">
      <q-card-section>
        <div class="text-h6 headers ">تغییرات</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="full-width q-mt-lg">
          <label class="labels">{{ 'نام دسته بندی  به ' + '   -   ' + update_data.old_name }}</label>
          <q-input input-style="text-align: center" v-model="update_data.new_name" class="inputs" square rounded
                   label-color="black" color="green-9" outlined dense></q-input>
        </div>
        <div class="full-width q-mt-lg">
          <label class="labels"> {{ 'توضیخات مربوط به ' + '    -   ' + update_data.old_description }}</label>
          <q-input type="textarea" maxlength="100" v-model="update_data.new_description"
                   input-style="text-align: center"
                   class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
        </div>
        <div class="full-width q-mt-lg">
          <label class="labels"> {{ 'مشخصات مربوط به ' + '    -   ' + update_data.string_text }}</label>
          <q-btn @click="AddRowUpdate" class="inputs" label="اضافه کردن مشخصات" square rounded label-color="white"
                 color="purple-8" outlined
                 dense></q-btn>
          <template v-for="(item  , index) in update_data.info_list" :key="index">
            <div class="row" style="width: 70% ; margin-right: 15% ; margin-left: 15%">
              <div class="col-md-8 ">
                <label class="labels"> مشخصه </label>
                <q-input type="text" maxlength="100" input-style="text-align: center"
                         v-model="update_data.info_list[index].name"
                         class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
              </div>
              <div class="col-md-4">
                <label class="labels"> </label>
                <q-btn @click='DeleteRowUpdate(index)' label="حذف کردن" class="inputs"
                       style="width: 60% ; margin-left: 20% ; margin-right: 20%"
                       rounded label-color="white" color="pink-6" outlined dense></q-btn>
              </div>
            </div>


          </template>
        </div>
        <div class="full-width q-mt-lg">
          <q-btn class="inputs" color="indigo-10" @click="updated" label="ثبت تغییرات"></q-btn>
        </div>
      </q-card-section>

      <q-card-actions align="left" class="bg-white text-pink-6">
        <q-btn flat label="خروج" v-close-popup class="text"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>


<script>
export default {
  name: "Stock"
}
</script>

<style scoped>

</style>
