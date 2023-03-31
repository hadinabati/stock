export  default class urls{
  constructor() {
    this.main = 'http://127.0.0.1:8000/'
  }

  position_list(){
    return this.main + 'positions/list'
  }
  position_create(){
    return this.main + 'positions/create'
  }
  position_update(){
    return this.main + 'positions/update'
  }
  Grade_list(){
    return this.main + 'grade/list'
  }
  Grade_create(){
    return this.main + 'grade/create'
  }
  Grade_update(){
    return this.main + 'grade/update'
  }
  Category_update(){
    return this.main + 'category/update'
  }
  Category_list(){
    return this.main + 'category/list'
  }
  Category_create(){
    return this.main + 'category/create'
  }
}
