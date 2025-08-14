import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useLoaderStore } from '@/stores/loader'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  // axiosのデフォルトのタイムアウト値は 0 です。これはタイムアウトしないことを意味します。
  // 一般的なAPI通信での設定: 5秒～15秒
  timeout: 10000
})

const refreshTokenApiClient = axios.create({
  withCredentials: true
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


apiClient.interceptors.request.use(
  (config) => {

    // POST, PUT, DELETEなどのリクエストに対してCSRFトークンをヘッダーに付与
    if (['POST', 'PUT', 'DELETE'].includes(config.method.toUpperCase())) {
      const csrfToken = getCookie('csrf_refresh_token'); // または csrf_access_token
      if (csrfToken) {
        config.headers['X-CSRF-TOKEN'] = csrfToken;
      }
    }

    // このファイルのような純粋なJavaScriptモジュールは、`import`文によって読み込まれた瞬間に、トップレベルのコードが即時評価（実行）されます
    // その一方、vueファイルは app.mount('#app')`が呼ばれたとで、`App.vue`コンポーネントのインスタンス化が始まる。
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
    if (error.response?.data?.error_code === "TOKEN_EXPIRED" && !originalRequest._refreshAttempt){
      console.log('TOKEN_EXPIRED - リフレッシュ開始')
      // originalRequest は単なるJavaScriptのオブジェクトなので、originalRequest['_refreshAttempt'] = true と書いても全く同じ
      originalRequest._refreshAttempt = true
      try{
        const response = await refreshTokenApiClient.post('/api/v1/auth/refresh-tokens', {}, {
            withCredentials: true
        })
        console.log('Access & Refreshトークン取得成功')
        if (response?.data.access_token){

          const authStore = useAuthStore()
          authStore.accessToken = response.data.access_token

          // 元のリクエストのヘッダーを更新
          originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
          // _refreshAttemptのフラグはこの部分で役に立つ。ここでループが発生しないように。
          try {
            const retryResponse = await apiClient(originalRequest);
            return retryResponse;
          } catch (retryError) {
            console.error('トークンリフレッシュ後の再試行に失敗しました。', retryError);
            console.error(retryError)
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

    return Promise.reject(error)
  }
)

export default apiClient