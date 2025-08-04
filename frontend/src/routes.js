import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// // layouts

// import PublicLayout from '@/layouts/PublicLayout.vue'
import AdminLayout  from '@/layouts/AdminLayout.vue'
import AuthLayout   from '@/layouts/AuthLayout.vue'
import PublicLayout from '@/layouts/PublicLayout.vue'


// public pages
import Home         from '@/views/public/Home.vue'
import Unauthorized from '@/views/public/Unauthorized.vue'
// import ProductList  from '@/views/products/ProductList.vue'
// import ProductDetail from '@/views/products/ProductDetail.vue'

// admin pages
import Users          from '@/views/admin/Users.vue'
import UserDetail     from '@/views/admin/UserDetail.vue'
import Furnitures     from '@/views/admin/Furnitures.vue'
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
    {
        path: '/',
        component: PublicLayout,
        children: [
            {
                path: 'unauthorized',
                name: 'unauthorized',
                component: Unauthorized,
            },
            {
                path: '',
                name: 'home',
                component: Home
            },
            // { path: 'products',    name: 'product-list',   component: ProductList },
            // { path: 'product/:id', name: 'product-detail', component: ProductDetail,  props: true,
            //     meta: { requiresAuth: true },
            // }
        ]
    },
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

    {
      path: '/admin',
        component: AdminLayout,
        children: [
          {
            path: 'users',
            name: 'users',
            component: Users,
            meta: { requiresAuth: true, requiresAdmin: true }
          },
          {
            path: 'user-detail/:id',
            name: 'user-detail',
            component: UserDetail,
            props: true,
            meta: { requiresAuth: true, requiresAdmin: true}
          },
          {
            path: 'furnitures',
            name: 'furnitures',
            component: Furnitures,
            meta: { requiresAuth: true, requiresAdmin: true}
          }
        ]


    },


    // {
    //     path: '/:catchAll(.*)', redirect: '/'
    // }
]



const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes
})

router.beforeEach(async(to)=>{
    const authStore = useAuthStore()
    console.log(`beforeEach呼ばれる`)
    // ★認証初期化がまだなら、完了するのを待つ
    if (!authStore.isInitialRefreshDone) {
        // 除外ルートでなければリフレッシュ処理を試みる
        const exclusionRoutes = ['login', 'register', 'home', 'unauthorized'];
        if (!exclusionRoutes.includes(to.name)) {
        await authStore.refreshOnReload();
    } else {
        // 除外ルートの場合は何もしないが、初期化完了フラグは立てる
        authStore.isInitialRefreshDone = true;
        }
    }

    console.log(`ログインされてる？${authStore.isAuthenticated}`)
    console.log(`管理者？？${authStore.isAdmin}`)
    console.log(`アクセストークン ${authStore.accessToken}`)
    if (to.meta.requiresAuth && !authStore.isAuthenticated){
        return { name: 'login' }
    }else if (to.meta.requiresAdmin && !authStore.isAdmin){
        return { name: 'unauthorized'}
    }
})



export default router


