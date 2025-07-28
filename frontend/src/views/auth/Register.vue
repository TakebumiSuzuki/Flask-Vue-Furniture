<script setup>
  import { reactive, ref } from 'vue'
  import axios from 'axios'

  const isLoading = ref(false)
  const formData = reactive({
    username: '',
    email: '',
    password: '',
    confirmation: '',
  })

  const handleSubmit = async () => {
    try{
      isLoading.value = true
      const response = await axios.post('/api/v1/auth/registration', {
        username: formData.username,
        email: formData.email,
        password: formData.password
      })
      console.log(response.data.username)
    }catch(err){
      console.log(`Failed to register ${err}`)

    }finally{
      isLoading.value = false
    }
  }
</script>

<template>
	<div class="relative py-[10%] max-w-[600px] w-full h-full mx-auto ">
		<div class="rounded-xl shadow-xl backdrop-blur-sm bg-white/60">
			<h1 class="text-4xl text-center py-8">Create Account</h1>

			<form @submit.prevent="handleSubmit" class="block w-full px-2 md:px-4 pb-14">

        <input
          type="text"
          placeholder="Username"
          v-model.trim="formData.username"
          class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500"
        >

				<input
          type="email"
          placeholder="Email"
          v-model.trim="formData.email"
          class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500"
        >

				<input
          type="password"
          placeholder="Password"
          v-model="formData.password"
          class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500"
        >

        <input
          type="password"
          placeholder="Password Confirmation"
          v-model="formData.confirmation"
          class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500"
        >

				<button
          type="submit"
          :disabled="isLoading"
          class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400"
        >
					Register Now
				</button>



			</form>


		</div>
	</div>

</template>