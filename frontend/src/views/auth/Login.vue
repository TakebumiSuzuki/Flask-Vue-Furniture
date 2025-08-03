<script setup>
  import { reactive, computed } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { loginSchema } from '@/schemas/user-validation.js'
  import { useLoaderStore } from '@/stores/loader'
  import { useRouter } from 'vue-router'
  import { useNotificationStore } from '@/stores/notification';

  import Login from '@/assets/icons/Login.svg'
  import Loader from '@/assets/icons/Loader.svg'

  import { useFormValidation } from '@/composables/userFormValidation'

  import authWrapper from '@/wrappers/authWrapper.vue';



  const isButtonDisabled = computed(()=>{
    return (!isFormValid.value || loaderStore.loading )
  })

  const loaderStore = useLoaderStore()
  const router = useRouter()
  const { login } = useAuthStore()
  const notificationStore = useNotificationStore();


  const formData = reactive({
    email: '',
    password: ''
  })

  const { isFormValid,
      errors,
      onInput,
      onBlur,
      validateOnSubmit,
      handleServerErrors} = useFormValidation(formData, loginSchema)

  const onSubmit = async ()=>{
    const cleanData = validateOnSubmit(formData)
      if (!cleanData){ return }

    try{
      await login(cleanData)
      router.push({name: 'user-info'})
      notificationStore.showNotification('You have successfully logged in!', 'success');

    }catch (err) {
      console.log('serverside error')
        handleServerErrors(err)
    }
  }

</script>

<template>
  <div>
    <authWrapper>
      <h1 class="text-4xl text-center pt-10 pb-4">Login</h1>

			<form @submit.prevent="onSubmit" class="block w-full px-2 md:px-4 pb-14" novalidate>

        <p class="validation-error-text !text-center"
            v-text="errors.root ? errors.root : ''"
        ></p>

        <div class="mb-4">
          <label for="email" class="sr-only">email</label>
          <p class="validation-error-text"
            v-text="errors.email ? errors.email : ''"
          ></p>
          <input
            type="email"
            id="email"
            placeholder="Email"
            :class="{ 'border-red-400': errors.email }"
            :value="formData.email"
            @input="onInput($event)"
            @blur="onBlur($event)"
            >
        </div>

        <div class="mb-4">
          <label for="password" class="sr-only">password</label>
          <p class="validation-error-text"
            v-text="errors.password ? errors.password : ''"
          ></p>
          <input
            type="password"
            id="password"
            placeholder="Password"
            :class="{'border-red-400': errors.password}"
            :value="formData.password"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
        </div>

				<button
          type="submit"
          class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400 mt-12
            disabled:!cursor-not-allowed disabled:!from-neutral-400 disabled:!to-neutral-500 disabled:!scale-100
          "
          :disabled="isButtonDisabled"
          >
          <div v-if="loaderStore.loading" class="flex items-center gap-2 justify-center">
            <Loader class="animate-spin"/>
            Processing
          </div>
          <div v-else class="flex items-center gap-2 justify-center">
            <Login/>
            Login
          </div>
				</button>
			</form>

		</authWrapper>
	</div>

</template>