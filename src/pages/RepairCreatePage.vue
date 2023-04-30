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
            <q-input  type="text" maxlength="100" input-style="text-align: center"
                     class="inputs" square rounded label-color="black" color="green-9" outlined dense></q-input>
          </div>
        </div>

        <div class="col-md-12">
          <div class="full-width q-mt-lg q-mb-md">
            <label class="labels"> دسته بندی</label>
            <q-select
                       option-value="id" option-label="name" dense color="green-9" outlined
                      square class="inputs" input-style="text-align: center ;">
            </q-select>
          </div>

        </div>

        <div class="col-md-6">
          <div class="full-width q-mt-lg">
            <label class="labels"></label>
            <q-btn color="indigo-10" class="inputs" label="اضافه کردن قسمت"></q-btn>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import {reactive} from "vue";
import urls from "src/Urls";

export default {
  name: "RepairCreatePage",
  data(){

    const  address = new urls()
    const  activity_info = reactive({
      name :'' ,
      category_list :[],
      properties :[]
    })
    



    return{

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
