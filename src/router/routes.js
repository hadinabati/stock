// import PositionPage from "pages/PositionPage.vue";
// import GradePage from "pages/GradePage.vue";
// import CategoryPage from "pages/CategoryPage.vue";
// import person from "pages/person.vue";
// import RolePage from "pages/RolePage.vue";
// import RoleListPage from "pages/RoleListPage.vue";
// import Stock from "pages/Stock.vue";
// import ProductPage from "pages/ProductPage.vue";
// import ActivityCreatePage from "pages/ActivityCreatePage.vue";
// import ActivityListPage from "pages/ActivityListPage.vue";
// import Repair from "pages/Repair.vue";
import Main_page from "pages/NewUI/Main_page.vue";

const routes = [
  // {
  //   path: '/',
  //   component: () => import('layouts/MainLayout.vue'),
  //   children: [
  //     {path: '', component: () => import('pages/IndexPage.vue')},
  //     {path: '/Position', component:PositionPage},
  //     {path: '/Grade', component:GradePage},
  //     {path: '/Category' , component:CategoryPage},
  //     {path:'/person'  , component:person},
  //     {path: '/create_role' , component:RolePage},
  //     {path: '/role_list' , component:RoleListPage},
  //     {path: '/stock' , component:Stock},
  //     {path: "/products" , component:ProductPage},
  //     {path: "/activity_create" , component:ActivityCreatePage},
  //     {path: '/activity_list' , component : ActivityListPage},
  //     {path:'/repair' , component:Repair}
  //
  //   ]
  // },
  {
    path: "/",
    component: () => import('pages/NewUI/Main_layout.vue'),
    children: [
      {path: '', component: Main_page}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Old_UI/ErrorNotFound.vue')
  }
]

export default routes