import { createWebHistory, createRouter } from "vue-router";
import LandingPageView from "./../views/LandingPageView.vue";
import AboutView from "./../views/AboutView.vue";
import DashboardView from "./../views/DashboardView.vue";
import MatchupView from "./../views/MatchupView.vue";
import StatisticsView from "./../views/StatisticsView.vue";
import AccountView from "./../views/AccountView.vue";
import PageNotFound from "@/views/PageNotFound.vue";
import store from './../store';

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPageView,
  },
  {
    path: "/about",
    name: "About",
    component: AboutView,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: "/matchup",
    name: "Matchup",
    component:MatchupView,
    meta: { requiresAuth: true },
  },
  {
    path: "/statistics",
    name: "Statistics",
    component: StatisticsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/account",
    name: "Account",
    component: AccountView,
    meta: { requiresAuth: true },
  },
  {
    path: '/:catchAll(.*)*',
    name: "PageNotFound",
    component: PageNotFound,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.isLoggedIn) {
      next({ name: 'LandingPage' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;