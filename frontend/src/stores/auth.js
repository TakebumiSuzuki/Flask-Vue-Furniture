import { defineStore } from 'pinia';
import { ref, computed } from 'vue'
import apiClient from '@/api';


export const useAuthStore = defineStore('auth', ()=>{

  const accessToken = ref(null)
  const user = ref(null)

  const isAuthenticated = computed(()=> Boolean(accessToken.value) )
  const isAdmin = computed(()=> user.value?.is_admin ?? false)



  async function createUser(formData){
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
    try{
      const { data } = await apiClient.post('/api/v1/auth/login', formData)
      accessToken.value = data.accessToken
      user.value = data.user

    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to log in. Please try again later'
      throw new Error(message)
    }
  }

  async function logout(){
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
    try{
      await apiClient.patch('/api/v1/update-username', formData)
      user.username = formData.username
    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to update username. Please try again later'
      throw new Error(message)
    }
  }

  async function updatePassword(formData){
    try{
      await apiClient.patch('/api/v1/update-password', formData)
      accessToken.value = null
      user.value = null
    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to change password. Please try again later'
      throw new Error(message)
    }
  }


  async function deleteUser(){
    try{
      await apiClient.delete('/api/v1/auth/delete')
      accessToken.value = null
      user.value = null
    }catch(err){
      const message = err?.response?.data?.message ?? 'Failed to delete this account. Please try again later'
      throw new Error(message)
    }


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
  }

})