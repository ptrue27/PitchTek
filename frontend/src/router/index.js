import { createWebHistory, createRouter } from "vue-router";
import LandingPageView from "./../views/LandingPageView.vue";
import AboutView from "./../views/AboutView.vue";
import DashboardView from "./../views/DashboardView.vue";
import StatisticsView from "./../views/StatisticsView.vue";
import HistoryView from "./../views/HistoryView.vue";

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
  },
  {
    path: "/statistics",
    name: "Statistics",
    component: StatisticsView,
  },
  {
    path: "/history",
    name: "History",
    component: HistoryView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;