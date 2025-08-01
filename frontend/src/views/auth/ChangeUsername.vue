<script setup>
  import { reactive, computed } from 'vue'
  import { useRouter } from 'vue-router'

  import { useAuthStore } from '@/stores/auth'
  import { useLoaderStore } from '@/stores/loader'
  import { changeUsernameSchema } from '@/schemas/user-validation'

  import authWrapper from '@/wrappers/authWrapper.vue';
  import Loader from '@/assets/icons/Loader.svg'
  import Check from '@/assets/icons/Check.svg'


  const router = useRouter()
  const authStore = useAuthStore()
  const loaderStore = useLoaderStore()

  const formData = reactive({
    newUsername: null,
  })
  const errors = reactive({
    root: null,
    newUsername: null
  })
  const activated = reactive({
    root: null,
    newUsername: null
  })

  const rootError = computed(() =>
    errors.root && activated.root ? errors.root : ''
  );

  const newUsernameError = computed(() =>
    errors.newUsername && activated.newUsername ? errors.newUsername : ''
  );

  function validateForm(formData){
    Object.keys(errors).forEach(key => { errors[key] = '' });
    const result = changeUsernameSchema.safeParse(formData)
    if (result.success){
      // errors.newUsername = null
      return result.data
    }else{
      const { formErrors, fieldErrors } = result.error.flatten();
      if (formErrors.length > 0) {
        errors.root = formErrors[0];
      }
      for (const key in fieldErrors) {
        const messages = fieldErrors[key];
        if (messages) {
          errors[key] = messages[0];
        }
      }
      return null
    }
  }

  const handleInput = (e)=>{
    formData.newUsername = e.target.value
    validateForm(formData)
  }

  const handleBlur = (e)=>{
    const result = validateForm(formData)
    if (!result){
      activated[e.target.id] = true
    }
  }

  const onSubmit = async ()=>{
    const cleanData = validateForm(formData)
    if (!cleanData){
      for (const key in errors){
        if (key){
          activated[key] = true
        }
      }
      return
    }
    try{
      await authStore.updateUsername(formData)
      router.push({name: 'user-info'})
      //メッセージを出す
    }catch(err){

    }
  }

</script>


<template>
  <div>
    <authWrapper>

      <h1 class="text-4xl text-center py-8">Create Account</h1>

      <form @submit.prevent="onSubmit" class="block w-full px-2 md:px-4 pb-14" novalidate>

        <div v-if="rootError">{{ rootError }}</div>

        <div class="mb-4">
          <label for="newUsername" class="sr-only">New Username</label>

          <p class="validation-error-text">
              {{ newUsernameError }}
          </p>

          <input
            type="text"
            id="newUsername"
            class="w-full"
            @input="handleInput($event)"
            :value="formData.newUsername"
            @blur="handleBlur($event)"
          >

        </div>


        <button type="submit" class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400 mt-12">
          <div v-if="loaderStore.loading" class="flex items-center gap-2 justify-center">
            <Loader class="animate-spin"/>
            Processing
          </div>
          <div v-else class="flex items-center gap-2 justify-center">
            <Check/>
            Change Username
          </div>
        </button>
      </form>


    </authWrapper>
  </div>
</template>