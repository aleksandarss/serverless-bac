import { createRouter, createWebHistory } from "vue-router";

const routes = [
    {
        path: "/",
        name: "Home",
        component: () =>
        import(/* webpackChunkName: "about" */ "../views/Home.vue"),
    },
    {
        path: "/about",
        name: "About",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
        import(/* webpackChunkName: "about" */ "../views/About.vue"),
    },
    {
        path: '/register',
        name: 'Register',
        component: () =>
        import(/* webpackChunkName: "register" */ '../views/Register.vue'),
    },
    {
        path: '/login',
        name: 'Login',
        component: () =>
            import(/* webpackChunkName: "login" */ '../views/Login.vue'),
    },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
