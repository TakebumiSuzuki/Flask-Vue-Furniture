import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useLoaderStore } from '@/stores/loader'

const apiClient = axios.create({
  // baseURL: 'http://localhost:5000',
  // axiosのデフォルトのタイムアウト値は 0 です。これはタイムアウトしないことを意味します。
  // 一般的なAPI通信での設定: 5秒～15秒
  timeout: 10000
})

const refreshTokenApiClient = axios.create({
  withCredentials: true
});


apiClient.interceptors.request.use(
  (config) => {
    // Vueコンポーネントではない、このような一般的なモジュールは、アプリケーションの他の部分が
    // 初期化される前にインポートされてコードが実行される可能性があるのでここで初期化。
    const loaderStore = useLoaderStore()
    loaderStore.increaseCount()

    // // app.use(pinia)が実行される前に、このモジュールがインポートされ、コードが評価される可能性があるので。
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
    console.log('200番台以外のAPIレスポンスが返ってきています。')
    if (error.response?.data?.error_code === "TOKEN_EXPIRED" && !originalRequest._refreshAttempt){
        console.log('TOKEN_EXPIREDのコードなのでリフレッシュを始めます')
        // originalRequest は単なるJavaScriptのオブジェクトなので、originalRequest['_refreshAttempt'] = true と書いても全く同じ
        originalRequest._refreshAttempt = true
        try{
            const response = await refreshTokenApiClient.post('/api/v1/auth/refresh-tokens', {}, {
                withCredentials: true
            })
            console.log('リフレッシュが終わりすでにAccess, refreshトークン両方を取得できました')
            if (response?.data.access_token){


                const authStore = useAuthStore()
                authStore.accessToken = response.data.access_token

                console.log('再度エラー前のAPIリクエスを送ります')
                // 元のリクエストのヘッダーを更新
                originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
                // _refreshAttemptのフラグはこの部分で役に立つ。ここでループが発生しないように。
                try {
                    const retryResponse = await apiClient(originalRequest);
                    return retryResponse;
                } catch (retryError) {
                    console.error('トークンリフレッシュ後の再試行に失敗しました。', retryError);
                    // 再試行の失敗もエラーとして扱う
                    return Promise.reject(retryError);
                }

            }
        }catch(refreshError){
            //ログアウト処理
            console.error('トークンのリフレッシュ処理自体に失敗しました。', refreshError);
            return Promise.reject(refreshError)
        }
    }
    console.log('TOKEN_EXPIREDのエラーではないので、そのままエラーを排出します')
    return Promise.reject(error)
  }
)

export default apiClient