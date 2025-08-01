<script setup>
  import { reactive, ref, computed } from 'vue'
  import { useRouter } from 'vue-router'

  import { useAuthStore } from '@/stores/auth'
  import { useLoaderStore } from '@/stores/loader'
  import { changePasswordSchema } from '@/schemas/user-validation'
  import apiClient from '@/api'

  import authWrapper from '@/wrappers/authWrapper.vue';
  import Loader from '@/assets/icons/Loader.svg'
  import Check from '@/assets/icons/Check.svg'

  const authStore = useAuthStore()
  const loaderStore = useLoaderStore()
  const router = useRouter()

  const isFormValid = ref(false)
  const isButtonDisabled = computed(()=>{
    return (!isFormValid.value || loaderStore.loading )
  })

  const formData = reactive({
    old_password: '',
    new_password: '',
    password_confirmation: ''
  })
  const errors = reactive({})

  const validateForm = (formData)=>{
    const result_raw = changePasswordSchema.safeParse(formData)
    if (result_raw.success){
      return { cleanData: result_raw.data, errors: null }
    }else{
      const errors = {}
      const { formErrors, fieldErrors } = result_raw.error.flatten();
      if (formErrors.length > 0) {
        errors['root'] = formErrors[0];
      }
      for (const key in fieldErrors) {
        const messages = fieldErrors[key];
        if (messages) {
          errors[key] = messages[0];
        }
      }
      return { cleanData: null, errors: errors}
    }
  }

  const onInput = (e)=>{
    const key = e.target.id
    formData[key] = e.target.value

    const result = validateForm(formData) // if節の中でなくここに書くのは、buttonのdisableのため
    isFormValid.value = Boolean(result.cleanData)

    if (key in errors){ //そのフィールドが追跡モードに入っていた場合
      errors[key] = ''
      if (result.errors?.[key]){
        errors[key] = result.errors[key]
      }
    }
  }
  const onBlur = (e)=>{
    const key = e.target.id
    const result = validateForm(formData)
    if (result.errors?.[key]){
      errors[key] = result.errors[key] //そのフィールドを追跡モードに入れる
    }
  }

  const onSubmit = async ()=>{
    Object.keys(errors).forEach(key => { errors[key] = '' });
    const result = validateForm(formData)
    if (result.errors){
      for (const key in result.errors){
        errors[key] = result.errors[key]
      }
      return
    }
    try{
      const response = await apiClient.patch({
        old_password: result.cleanData.old_password,
        new_password: result.cleanData.new_password
      })
      authStore.accessToken = null
      authStore.user = null
      router.push({name: 'login'})
      //notificationの表示をする

    }catch(err){
      console.log('serverside error')
    }


  }

</script>

<template>
  <div>
    <authWrapper>

      <h1 class="text-4xl text-center pt-10 pb-4">Change Password</h1>

      <form @submit.prevent="onSubmit" class="block w-full px-2 md:px-4 pb-14" novalidate>

        <p class="validation-error-text text-center"
            v-text="errors.root ? errors.root : ''"
        ></p>

        <div class="mb-4">
          <label for="old_password" class="sr-only">Current Password</label>
          <p class="validation-error-text"
            v-text="errors.old_password ? errors.old_password : ''"
          ></p>
          <input
            type="password"
            id="old_password"
            placeholder="Current Password"
            :class="{'border-red-400': errors.old_password}"
            :value="formData.old_password"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
        </div>

        <div class="mb-4">
          <label for="new_password" class="sr-only">New Password</label>
          <p class="validation-error-text"
            v-text="errors.new_password ? errors.new_password : ''"
          ></p>
          <input
            type="password"
            id="new_password"
            placeholder="New Password"
            :class="{'border-red-400': errors.new_password}"
            :value="formData.new_password"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
        </div>

        <div class="mb-4">
          <label for="password_confirmation" class="sr-only">Password Confirmation</label>
          <p class="validation-error-text"
            v-text="errors.password_confirmation ? errors.password_confirmation : ''"
          ></p>
          <input
            type="password"
            id="password_confirmation"
            placeholder="Enter new password again"
            :class="{'border-red-400': errors.password_confirmation }"
            :value="formData.password_confirmation"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
        </div>


        <button
          type="submit"
          class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400 mt-12 "
          :class="{
            '!cursor-not-allowed': isButtonDisabled,
            '!from-neutral-400': isButtonDisabled,
            '!to-neutral-400': isButtonDisabled,
            '!scale-100': isButtonDisabled,
          }"
          :disabled="isButtonDisabled"
        >
          <div v-if="loaderStore.loading" class="flex items-center gap-2 justify-center">
            <Loader class="animate-spin"/>
            Processing
          </div>
          <div v-else class="flex items-center gap-2 justify-center">
            <Check/>
            Change Password
          </div>
        </button>
      </form>


    </authWrapper>
  </div>
</template>