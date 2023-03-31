import PositionPage from "pages/PositionPage.vue";
import GradePage from "pages/GradePage.vue";
import CategoryPage from "pages/CategoryPage.vue";

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/IndexPage.vue')},
      {path: '/Position', component:PositionPage},
      {path: '/Grade', component:GradePage},
      {path: '/Category' , component:CategoryPage}
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
