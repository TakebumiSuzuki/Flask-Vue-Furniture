<script setup>
  import { reactive, ref, computed } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { createUserSchema } from '@/schemas/user-validation.js'
  import { useLoaderStore } from '@/stores/loader'
  import { useRouter } from 'vue-router'

  import CheckIcon from '@/assets/icons/Check.svg'
  import LoaderIcon from '@/assets/icons/Loader.svg'

  const loaderStore = useLoaderStore()
  const router = useRouter()
  const { createUser } = useAuthStore()

  const usernameError = computed(() =>
    errors.username && activated.username ? errors.username : ''
  );
  const emailError = computed(() =>
    errors.email && activated.email ? errors.email : ''
  );
  const passwordError = computed(() =>
    errors.password && activated.password ? errors.password : ''
  );
  const password_confirmationError = computed(() =>
    errors.password_confirmation && activated.password_confirmation ? errors.password_confirmation : ''
  );

  const formData = reactive({
    username: '',
    email: '',
    password: '',
    password_confirmation: '',
  })

  const errors = reactive({
    root: '',
    username: '',
    email: '',
    password: '',
    password_confirmation: '',
  })

  const activated = reactive({
    root: false,
    username: false,
    email: false,
    password: false,
    password_confirmation: false,
  })

  function validateForm(formData){
    // フォーム送信時にエラーを一旦リセットする（任意ですが推奨）
    Object.keys(errors).forEach(key => { errors[key] = '' });

    const result = createUserSchema.safeParse(formData)

    if (result.success) {

      return result.data

    }else{
      // flatten() を使ってエラーを整形されたオブジェクトとして取得
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

  function onInput(field, e) {
    formData[field] = e.target.value
    validateForm(formData)
  }

  function onBlur(field, e) {
    if (errors[field]){
      activated[field] = true
    }
  }

  async function onSubmit() {
    const cleanedData = validateForm(formData)
    if (!cleanedData){
      for (const key in errors){
        if (key){
          activated[key] = true
        }
      }
      return
    }

    const { password_confirmation, ...payload } = cleanedData
    try {
      await createUser(payload)
      router.push({name: 'login'})
      // 成功のNotification→ログインしてください、と。

    } catch (err) {
      // console.error(err)
      // if (err.response?.data){
      //   if (err.response.data.error_code === 'VALIDATION_ERROR') {
      //     for (const key in err.response.data.details) {
      //       if (Object.hasOwn(errors, key)) { // errorsオブジェクトに存在するキーか確認
      //         errors[key] = err.response.data.details[key];
      //       }
      //     }
      //   }else if (err.response.data.error_code === 'Conflict'){
      //     // `errors.append` ではなく、`errors.root` に代入する
      //     errors.root = err.response.data.message;
      //   }
      // }
    }
  }
</script>

<template>
  <div class="relative pt-[10%] max-w-[600px] w-full h-full mx-auto ">

    <div class="rounded-xl shadow-xl backdrop-blur-sm bg-white/60">

      <h1 class="text-4xl text-center py-8">Create Account</h1>

      <form @submit.prevent="onSubmit" class="block w-full px-2 md:px-4 pb-14" novalidate>
        <div v-if="errors.root && activated.root"></div>

        <!-- ユーザー名入力 -->
        <div class="mb-4">

          <label for="username" class="sr-only">Username</label>
          <p class="validation-error-text">
            {{ usernameError }}
          </p>

          <input
            id="username"
            type="text"
            placeholder="Username"
            :value="formData.username"
            @input="onInput('username', $event)"
            @blur="onBlur('username', $event)"
            class="w-full"
            :class="{ 'border-red-400': usernameError }"
          />
        </div>

        <div class="mb-4">
          <label for="email" class="sr-only">Email</label>
          <p class="validation-error-text">
            {{ emailError }}
          </p>
          <input
            id="email"
            type="email"
            placeholder="Email"
            :value="formData.email"
            @input="onInput('email', $event)"
            @blur="onBlur('email', $event)"
            class="w-full"
            :class="{ 'border-red-400': emailError }"
          />
        </div>

        <div class="mb-4">
          <label for="password" class="sr-only">Password</label>
          <p class="validation-error-text">
            {{ passwordError }}
          </p>
          <input
            id="password"
            type="password"
            placeholder="Password"
            :value="formData.password"
            @input="onInput('password', $event)"
            @blur="onBlur('password', $event)"
            class="w-full"
            :class="{ 'border-red-400': passwordError }"
          />
        </div>

        <div class="mb-4">
          <label for="password-confirmation" class="sr-only">Password Confirmation</label>
          <p class="validation-error-text">
            {{ password_confirmationError }}
          </p>
          <input
            id="password-confirmation"
            type="password"
            placeholder="Password Confirmation"
            :value="formData.password_confirmation"
            @input="onInput('password_confirmation', $event)"
            @blur="onBlur('password_confirmation', $event)"
            class="w-full"
            :class="{ 'border-red-400': password_confirmationError }"
          />
        </div>

        <button
          type="submit"
          :disabled="loaderStore.loading"
          class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400 mt-12"
        >
          <div v-if="loaderStore.loading" class="flex items-center justify-center gap-1" >
            <LoaderIcon class="animate-spin"/>
            Processing
          </div>
          <div v-else class="flex items-center justify-center gap-1 ">
            <CheckIcon/>
            Register Now
          </div>
        </button>
      </form>

    </div>
  </div>

</template>
