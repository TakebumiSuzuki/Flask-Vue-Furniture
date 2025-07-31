import axios from 'axios'
import { useLoaderStore } from '@/stores/loader'
import { useAuthStore } from '@/stores/auth'

const apiClient = axios.create({
    // axiosのデフォルトのタイムアウト値は 0 です。これはタイムアウトしないことを意味します。
    // 一般的なAPI通信での設定: 5秒～15秒
    timeout: 10000
})


apiClient.interceptors.request.use(
    (config) => {
        // Vueコンポーネントではない、このような一般的なモジュールは、アプリケーションの他の部分が
        // 初期化される前にインポートされてコードが実行される可能性があるのでここで初期化。
        const loaderStore = useLoaderStore()
        loaderStore.increaseCount()

        const authStore = useAuthStore()
        if (authStore.accessToken){
            config.headers.Authorization = `Bearer ${authStore.accessToken}`
        }
        return config
    },
    (error) => {
        const loaderStore = useLoaderStore()
        loaderStore.decreaseCount()

        // ★改善点2: エラーを後続に伝える
        return Promise.reject(error)
    }
)
// # (1) refresh=True: リフレッシュトークンのみを許可
// # (2) locations=["cookies"]: トークンはCookieからのみ探す
// @jwt_required(refresh=True, locations=["cookies"])

apiClient.interceptors.response.use(
    (response) => {
        const loaderStore = useLoaderStore()
        loaderStore.decreaseCount()
        return response
    },

    async (error) => {
        // この部分は200番台以外の時(タイムアウトやCORSエラーなども含む)にもちゃんと呼ばれる
        const loaderStore = useLoaderStore()
        loaderStore.decreaseCount()

        const originalRequest = error.config;

        if (error.response?.data?.error_code === "TOKEN_EXPIRED" && !originalRequest._refreshAttempt){

            originalRequest._refreshAttempt = true
            try{
                const response = await apiClient.post('/api/v1/auth/refresh-tokens', {}, { withCredentials: true })
                if (response?.data.accessToken){
                    const authStore = useAuthStore()
                    authStore.accessToken = response.data.accessToken

                    const retryResponse = await apiClient(originalRequest)
                    return retryResponse
                }
            }catch(refreshError){
                //ログアウト処理
                return Promise.reject(refreshError)
            }
        }
        return Promise.reject(error)
    }
)

export default apiClient