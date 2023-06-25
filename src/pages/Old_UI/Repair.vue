<template>
  <div class="row q-mt-lg" style="margin-top: 5rem">
    <div class="col-md-2"></div>
    <div class="col-md-4">
      <q-card class="shadow-6 q-ma-md bg-teal-3" style="height: 400px">
        <q-btn @click="Form1" label="فرم گردشگار کالاهای غیر مصرفی" class="absolute-center btn" stack text-color="dark"
               glossy></q-btn>
      </q-card>
    </div>

    <div class="col-md-4">
      <q-card  class="shadow-6 q-ma-md bg-teal-3" style="height: 400px">
        <q-btn @click="Form2" label="فرم گردشگار کالاهای  مصرفی" class="absolute-center btn" stack text-color="dark"
               glossy></q-btn>
      </q-card>
    </div>
    <div class="col-md-2"></div>
  </div>


  <q-dialog v-model="Forms.form1" full-width full-height>
    <q-card>
      <q-card-section>
        <div class="text-h6 headers" >گردشکار کالاهای مصرفی</div>
      </q-card-section>
      <Form1Component :stock_number="0" :read_only="false"></Form1Component>
      <q-card-section class="q-pt-none">

      </q-card-section>
      <q-card-actions align="right">
        <q-btn  class="absolute-bottom-right q-ma-md" stack text-color="white"  label="بستن پنجره" color="pink-6" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="Forms.form2" full-width full-height>
    <q-card>
      <q-card-section>
        <div class="text-h6 headers">گردشکار کالاهای مصرفی</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
       <Form2Component></Form2Component>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn  class="absolute-bottom-right q-ma-md" stack text-color="white"  label="بستن پنجره" color="pink-6" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>


</template>

<script>
import Form1Component from "pages/Old_UI/Form1Component.vue";
import Form2Component from "pages/Old_UI/Form2Component.vue";
import {reactive} from "vue";

export default {
  name: "Repair",
  components: {
    Form1Component,
    Form2Component
  },
  data() {
    const Forms = reactive({
      form1: false,
      form2: false
    })
    function form1(){

    }


    return{
      Forms,
      form1
    }

  },

  methods:{
    Form1(){
      this.Forms.form1 = true
      this.Forms.form2 = false
    },
    Form2(){
      this.Forms.form2 = true
      this.Forms.form1 = false
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

.btn {
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
