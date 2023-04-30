import PositionPage from "pages/PositionPage.vue";
import GradePage from "pages/GradePage.vue";
import CategoryPage from "pages/CategoryPage.vue";
import person from "pages/person.vue";
import RolePage from "pages/RolePage.vue";
import RoleListPage from "pages/RoleListPage.vue";
import Stock from "pages/Stock.vue";
import ProductPage from "pages/ProductPage.vue";
import RepairCreatePage from "pages/RepairCreatePage.vue";

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/IndexPage.vue')},
      {path: '/Position', component:PositionPage},
      {path: '/Grade', component:GradePage},
      {path: '/Category' , component:CategoryPage},
      {path:'/person'  , component:person},
      {path: '/create_role' , component:RolePage},
      {path: '/role_list' , component:RoleListPage},
      {path: '/stock' , component:Stock},
      {path: "/products" , component:ProductPage},
      {path: "/repair_create" , component:RepairCreatePage}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
