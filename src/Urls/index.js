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
  person_create(){
    return this.main + 'person/create'
  }
  person_list(){
    return this.main + 'person/list'
  }

  person_active(){
    return this.main + 'person/active'
  }
  person_delete(){
    return this.main + 'person/delete'
  }
  person_update(){
    return this.main + 'person/update'
  }

  role_create(){
    return this.main + 'role/create'
  }
  role_list(){
    return this.main + 'role/lists'
  }
  role_deleted(){
    return this.main + 'role/deleted'
  }
  role_activated(){
    return this.main + 'role/activated'
  }

  route_list(){
    return this.main + 'routes/lists'
  }
  route_update(){
    return this.main + 'routes/check'
  }

  stock_create(){
    return this.main + 'stock/create'
  }
  stock_list(){
    return this.main + 'stock/list'
  }
  stock_list_single(){
    return this.main + 'stock/list_single'
  }
  stock_list_is_consumere(){
    return this.main + 'stock/list_is_consumer'
  }

  activities_create(){
    return this.main + 'activities/create'
  }
  activities_list(){
    return this.main + 'activities/list'
  }
  activities_delete(){
    return this.main + 'activities/delete'
  }
  activities_active(){
    return this.main + 'activities/active'
  }

  repair_create(){
    return this.main + 'repair/create'
  }


}
