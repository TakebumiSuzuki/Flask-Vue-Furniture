import { createRouter, createWebHistory } from 'vue-router'


// // layouts
// import PublicLayout from '@/layouts/PublicLayout.vue'
// import AdminLayout  from '@/layouts/AdminLayout.vue'
import AuthLayout   from '@/layouts/AuthLayout.vue'

// // public pages
// import Home         from '@/views/home/Home.vue'
// import ProductList  from '@/views/products/ProductList.vue'
// import ProductDetail from '@/views/products/ProductDetail.vue'

// // admin pages
// import Items        from '@/views/admin/Items.vue'
// import Item         from '@/views/admin/Item.vue'
// import CreateItem   from '@/views/admin/CreateItem.vue'
// import EditItem     from '@/views/admin/EditItem.vue'

// auth pages
import Login          from '@/views/auth/Login.vue'
import Register       from '@/views/auth/Register.vue'
import ChangeUsername from '@/views/auth/ChangeUsername.vue'
import ChangePassword from '@/views/auth/ChangePassword.vue'
import UserInfo       from '@/views/auth/UserInfo.vue'

// import Unauthorized from '@/views/error/Unauthorized.vue'


const routes = [
    // {
    //     path: '/',
    //     component: PublicLayout,
    //     children: [
    //         { path: '',            name: 'home',           component: Home },
    //         { path: 'products',    name: 'product-list',   component: ProductList },
    //         { path: 'product/:id', name: 'product-detail', component: ProductDetail,  props: true,
    //             meta: { requiresAuth: true },
    //         }
    //     ]
    // },
    // {
    //     path: '/admin',
    //     component: AdminLayout,
    //     meta: { requiresAuth: true, requiresAdmin: true }, // ★ このルートとその子ルートは認証が必要
    //     children: [
    //         { path: 'items',            name: 'admin-items',         component: Items },
    //         { path: 'items/create',     name: 'admin-item-create',   component: CreateItem },
    //         { path: 'items/:id',        name: 'admin-item-detail',   component: Item,          props: true },
    //         { path: 'items/:id/edit',   name: 'admin-item-edit',     component: EditItem,      props: true },
    //     ]
    // },
    {
        path: '/auth',
        component: AuthLayout,
        children: [
            {
                path: 'login', // ここを'/login'と書くと、'/auth'が置き換えられてしまうので'login'と書くのが正解
                name: 'login',
                component: Login,
            },
            {
                path: 'register',
                name: 'register',
                component: Register,
            },
            {
                path: 'change-username',
                name: 'change-username',
                component: ChangeUsername,
                meta: { requiresAuth: true },
            },
            {
                path: 'change-password',
                name: 'change-password',
                component: ChangePassword,
                meta: { requiresAuth: true },
            },
            {
                path: 'user-info',
                name: 'user-info',
                component: UserInfo,
                meta: { requiresAuth: true },
            }
        ]
    },
    // ★ 権限がない場合に表示するページ用のルートを追加
    // {
    //     path: '/unauthorized',
    //     component: PublicLayout,
    //     children: [
    //         { path: '',   name: 'unauthorized', component: Unauthorized }
    //     ]
    // },

    // {
    //     path: '/:catchAll(.*)', redirect: '/'
    // }
]



const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes
})



export default router


