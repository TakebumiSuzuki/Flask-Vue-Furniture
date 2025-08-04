import { defineStore } from 'pinia';
import { ref, computed } from 'vue'
import  axios  from 'axios'
const refreshTokenApiClientOnReload = axios.create({
    withCredentials: true
});

export const useAuthStore = defineStore('auth', ()=>{

  const accessToken = ref(null)
  const user = ref(null)

  const isAuthenticated = computed(()=> Boolean(accessToken.value) )
  const isAdmin = computed(()=> user.value?.is_admin ?? false)

  let isInitialRefreshDone = false

  async function createUser(formData){
    const apiClient = (await import('@/api')).default

    try{
      const { data } = await apiClient.post('/api/v1/auth/registration', formData)

    }catch(err){
      if (err.response?.data) {
        const errorData = err.response.data;

        //【修正点1】バリデーションエラーの場合
        if (errorData.error_code === 'VALIDATION_ERROR') {
          const formattedErrors = {};
          errorData.message.forEach(currentError => {
            const fieldName = currentError.loc[0];
            const message = currentError.msg;
            formattedErrors[fieldName] = message;
          });

          // Errorオブジェクトに汎用的なメッセージを設定
          const error = new Error('Validation failed. Please check the input values.');

          // カスタムプロパティとして、整形したエラーオブジェクトとエラータイプを追加
          // JavaScriptのオブジェクトは非常に柔軟で、作成後でも新しいプロパティを自由に追加できます。
          error.details = formattedErrors;
          error.type = 'VALIDATION_ERROR';

          throw error; // このカスタムエラーオブジェクトをスローする

        //【修正点2】コンフリクトエラーの場合
        } else if (errorData.error_code === 'Conflict') {
          const error = new Error(errorData.message); // メッセージはサーバーからのものをそのまま利用
          error.type = 'CONFLICT_ERROR'; // タイプを追加
          throw error;
        }
      }

      //【修正点3】上記以外の予期せぬエラーの場合
      // 汎用的なエラーをスローする
      throw new Error('Failed to register. Please try again later.');
    }

  }

  async function login(formData){
    const apiClient = (await import('@/api')).default

    try{
      const { data } = await apiClient.post('/api/v1/auth/login', formData)
      accessToken.value = data.access_token
      user.value = data.user

    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to log in. Please try again later'
      throw new Error(message)
    }
  }

  async function logout(){
    const apiClient = (await import('@/api')).default

    try{
      await apiClient.post('/api/v1/auth/logout', {}, { withCredentials: true })
      accessToken.value = null
      user.value = null
    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to log out. Please try again later'
      throw new Error(message)
    }
  }


  async function updateUsername(formData){
    const apiClient = (await import('@/api')).default

    try{
      await apiClient.patch('/api/v1/account/update-username', formData)
      user.username = formData.username
    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to update username. Please try again later'
      throw new Error(message)
    }
  }

  async function updatePassword(formData){
    const apiClient = (await import('@/api')).default

    try{
      await apiClient.patch('/api/v1/account/update-password', formData)
      accessToken.value = null
      user.value = null
    }catch(err){
      console.log(err)
      const message = err?.response?.data?.message ?? 'Failed to change password. Please try again later'
      throw new Error(message)
    }
  }


  async function deleteUser(){
    const apiClient = (await import('@/api')).default

    try{
      await apiClient.delete('/api/v1/account')
      accessToken.value = null
      user.value = null
    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to delete this account. Please try again later'
      throw new Error(message)
    }
  }

  async function deleteOtherUser(user_id){
    const apiClient = (await import('@/api')).default
    try{
      await apiClient.delete(`/api/v1/admin/users/${user_id}/delete-user`)
    }catch(err){
      console.log('ユーザー削除失敗')
    }
  }

  async function changeIsAdmin(user_id){
    const apiClient = (await import('@/api')).default
    try{
      await apiClient.patch(`/api/v1/admin/users/${user_id}/change-role`)
    }catch(err){
      console.log('ユーザー削除失敗')
    }
  }


  async function refreshOnReload(){
    console.log('リロードのリフレッシュを始めます')
    if (!isInitialRefreshDone){
      const response = await refreshTokenApiClientOnReload.post('/api/v1/auth/refresh-tokens', {}, {
        withCredentials: true
      })

      if (response?.data.access_token){
        console.log('リロードのリフレッシュでアクセストークンをゲットしました')
        accessToken.value = response.data.access_token
        // const response = await refreshTokenApiClientOnReload.post('/api/v1/auth/refresh-tokens')
        // response.data

      }else{
        console.log('リロードのリフレッシュでアクセストークンの取得に失敗しました')
      }
    }
    isInitialRefreshDone = true
  }


  return {
    accessToken,
    user,
    isAuthenticated,
    isAdmin,
    createUser,
    login,
    logout,
    updateUsername,
    updatePassword,
    deleteUser,
    deleteOtherUser,
    changeIsAdmin,
    refreshOnReload,
  }

},{
    persist: true, // ここで永続化を有効にする
  }
)