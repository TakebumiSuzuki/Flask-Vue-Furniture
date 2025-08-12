<script setup>
  import { reactive, computed } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { createUserSchema } from '@/schemas/user-validation.js'
  import { useLoaderStore } from '@/stores/loader'
  import { useRouter } from 'vue-router'
  import { useNotificationStore } from '@/stores/notification';

  import Check from '@/assets/icons/Check.svg'
  import Loader from '@/assets/icons/Loader.svg'

  import { useFormValidation } from '@/composables/userFormValidation'

  import authWrapper from '@/wrappers/authWrapper.vue';

  const isButtonDisabled = computed(()=>{
    return (!isFormValid.value || loaderStore.loading )
  })


  const loaderStore = useLoaderStore()
  const router = useRouter()
  const { createUser } = useAuthStore()
  const notificationStore = useNotificationStore();


  const formData = reactive({
    username: '',
    email: '',
    password: '',
    password_confirmation: '',
  })

  const { isFormValid,
      errors,
      onInput,
      onBlur,
      validateOnSubmit,
      handleServerErrors} = useFormValidation(formData, createUserSchema)


  async function onSubmit() {
    const cleanData = validateOnSubmit(formData)
      if (!cleanData){ return }

    const { password_confirmation, ...payload } = cleanData
    try {
      await createUser(payload)
      notificationStore.pendingNotification = { msg:'Registration done! Please log in!' ,msgType: 'success' }
      router.push({name: 'login'})

    } catch (err) {
      console.log('serverside error')
        handleServerErrors(err)
    }
  }

</script>

<template>
  <div>
    <authWrapper>
      <div class="block w-full px-4 pt-4 font-mideum text-teal-600">
        <RouterLink :to="{name: 'home'}">
          <div class=" size-fit px-0.5 animated-underline">
            &laquo; Home
          </div>
        </RouterLink>
      </div>

      <h1 class="text-4xl text-center pt-4 pb-4">Create Account</h1>

      <form @submit.prevent="onSubmit" class="block w-full px-2 md:px-4 pb-14" novalidate>

        <p class="validation-error-text !text-center">{{ errors.errors || '\u00A0' }}</p>

        <div class="mb-4">
          <label for="username" class="sr-only">Username</label>
          <p class="validation-error-text">{{ errors.username || '\u00A0' }}</p>
          <input
            type="text"
            id="username"
            placeholder="Username"
            :class="{ 'border-red-400': errors.username }"
            :value="formData.username"
            @input="onInput($event)"
            @blur="onBlur($event)"
          />
        </div>

        <div class="mb-4">
          <label for="email" class="sr-only">Email</label>
          <p class="validation-error-text">{{ errors.email || '\u00A0' }}</p>
          <input
            type="email"
            id="email"
            placeholder="Email"
            :class="{ 'border-red-400': errors.email }"
            :value="formData.email"
            @input="onInput($event)"
            @blur="onBlur($event)"
          />
        </div>

        <div class="mb-4">
          <label for="password" class="sr-only">Password</label>
          <p class="validation-error-text">{{ errors.password || '\u00A0' }}</p>
          <input
            type="password"
            id="password"
            placeholder="Password"
            :class="{'border-red-400': errors.password}"
            :value="formData.password"
            @input="onInput($event)"
            @blur="onBlur($event)"
          />
        </div>

        <div class="mb-4">
          <label for="password_confirmation" class="sr-only">Password Confirmation</label>
          <p class="validation-error-text">{{ errors.password_confirmation || '\u00A0' }}</p>
          <input
            type="password"
            id="password_confirmation"
            placeholder="Enter password again"
            :class="{'border-red-400': errors.password_confirmation }"
            :value="formData.password_confirmation"
            @input="onInput($event)"
            @blur="onBlur($event)"
          />
        </div>

        <button
          type="submit"
          class="btn w-full bg-gradient-to-br from-teal-400 to-teal-600 mt-12
            disabled:!cursor-not-allowed disabled:!from-neutral-400 disabled:!to-neutral-500 disabled:!scale-100
          "
          :disabled="isButtonDisabled"
        >
          <div v-if="loaderStore.loading" class="flex items-center gap-2 justify-center">
            <Loader class="animate-spin size-6 text-neutral-50"/>
            Processing
          </div>
          <div v-else class="flex items-center gap-2 justify-center">
            <Check class="size-5"/>
            Register Now
          </div>
        </button>
        <RouterLink :to="{name: 'login'}">
          <p class="pt-1 font-medium text-right mr-2 text-teal-600/90 transition duration-300 ease-in-out">You have an account?</p>
        </RouterLink>
      </form>

    </authWrapper>
  </div>
</template>
