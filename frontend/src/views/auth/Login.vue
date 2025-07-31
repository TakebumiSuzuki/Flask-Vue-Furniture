<script setup>
  import { reactive, ref } from 'vue'
  import { useLoaderStore } from '@/stores/loader'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'

  import Login from '@/assets/icons/Login.svg'
  import Loader from '@/assets/icons/Loader.svg'

  const loaderStore = useLoaderStore()
  const authStore = useAuthStore()
  const router = useRouter()

  const formData = reactive({
    email: null,
    password: null
  })
  const errors = ref(null)

  const handleSubmit = async ()=>{
    if (!formData.email || !formData.password){
      errors.value = 'Please enter values.'
      return
    }
    errors.value = null

    try{
      await authStore.login(formData)
      router.push({name: 'home'})
      // notification ここに
    }catch(err){
      errors.value = err.message
    }
  }

</script>

<template>
	<div class="relative pt-[10%] max-w-[600px] w-full h-full mx-auto ">

    <div class="rounded-xl shadow-xl backdrop-blur-sm bg-white/60">

      <h1 class="text-4xl text-center py-8">Login</h1>

			<form @submit.prevent="handleSubmit" class="block w-full px-2 md:px-4 pb-14" novalidate>

        <p v-text="errors ? '{{errors}}':''" class="text-sm h-5 mb-4 text-center text-red-400"></p>

        <div>
          <label for="email" class="sr-only">email</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500"
            v-model.trim="formData.email"
            >
        </div>

        <div>
          <label for="password" class="sr-only">password</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500"
            v-model="formData.password"
          >
        </div>

				<button type="submit" class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400" >
					<div v-if="loaderStore.loading" class="flex items-center justify-center gap-2">
            <Loader class="animate-spin" />
            Processing
          </div>
          <div v-else class="flex items-center justify-center gap-2">
            <Login/>
            Log In
          </div>
				</button>
			</form>

		</div>
	</div>

</template>