<script setup>
  import { reactive, computed } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { changeUsernameSchema } from '@/schemas/user-validation'
  import { useLoaderStore } from '@/stores/loader'
  import { useRouter } from 'vue-router'
  import { useNotificationStore } from '@/stores/notification';

  import Loader from '@/assets/icons/Loader.svg'
  import Check from '@/assets/icons/Check.svg'

  import { useFormValidation } from '@/composables/userFormValidation'

  import authWrapper from '@/wrappers/authWrapper.vue';

  const isButtonDisabled = computed(()=>{
    return (!isFormValid.value || loaderStore.loading )
  })

  const router = useRouter()
  const { updateUsername, user } = useAuthStore()
  const loaderStore = useLoaderStore()
  const notificationStore = useNotificationStore();

  const formData = reactive({
    username: '',
  })

  const { isFormValid,
      errors,
      onInput,
      onBlur,
      validateOnSubmit,
      handleServerErrors} = useFormValidation(formData, changeUsernameSchema)


  const onSubmit = async ()=>{
    const cleanData = validateOnSubmit(formData)
    if (!cleanData){ return }

    try{
      await updateUsername(cleanData)
      user.username = cleanData.username
      notificationStore.pendingNotification = { msg:'Username has been updated.' ,msgType: 'success' }
      router.push({name: 'user-info'})
    }catch (err) {
      console.log('serverside error')
        handleServerErrors(err)
    }
  }

</script>


<template>
  <div>
    <authWrapper>

      <h1 class="text-4xl text-center pt-10 pb-4">Change Username</h1>

      <form @submit.prevent="onSubmit" class="block w-full px-4 pb-14" novalidate>

        <p class="validation-error-text !text-center"
            v-text="errors.root ? errors.root : ''"
        ></p>

        <div class="mb-4">
          <label for="username" class="sr-only">New Username</label>

          <p class="validation-error-text"
            v-text="errors.username ? errors.username : ''"
          ></p>

          <input
            type="text"
            id="username"
            placeholder="Enter new username"
            :class="{ 'border-red-400': errors.username }"
            :value="formData.username"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >

        </div>


        <button
          type="submit"
          class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400 mt-12
            disabled:!cursor-not-allowed disabled:!from-neutral-400 disabled:!to-neutral-500 disabled:!scale-100"
          :disabled="isButtonDisabled"
        >
          <div v-if="loaderStore.loading" class="flex items-center gap-2 justify-center">
            <Loader class="animate-spin size-5.5 text-neutral-50"/>
            Processing
          </div>
          <div v-else class="flex items-center gap-2 justify-center">
            <Check class="size-5"/>
            Chage Username
          </div>
        </button>
      </form>

    </authWrapper>
  </div>
</template>