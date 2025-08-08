<script setup>
  import { onMounted, ref, computed } from 'vue'
  import apiClient from '@/api'
  import adminWrapper from '@/wrappers/adminWrapper.vue'
  import { useLoaderStore } from '@/stores/loader'
  import LoaderIcon from  '@/assets/icons/Loader.svg'

  const props = defineProps({ id: String })
  const loaderStore = useLoaderStore()
  const user = ref(null)

  const adminStatus = computed(()=>{
    return user.value.is_admin ? 'yes':'no'
  })


  onMounted(async ()=>{
    try{
      const result = await apiClient.get(`/api/v1/admin/users/${props.id}`)
      if (result.data){
        console.log(result.data.user)
        user.value = result.data.user
      }

    }catch(err){
      console.log(err)
    }
  })


</script>

<template>
  <adminWrapper>
    <div class="px-2 md:px-4 md:border-l min-h-180 border-neutral-500">
      <h1 class="text-center text-4xl tracking-widest">User Info</h1>


        <div class="max-w-[600px] w-full mx-auto mt-4 pb-24 ">
          <RouterLink :to="{name: 'users'}">
            <div class="text-neutral-300 size-fit px-0.5 animated-underline">
              &laquo; Go Back
            </div>
          </RouterLink>
          <div v-if="user && !loaderStore.loading" class="mt-6">
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">ID:</p>
              <p class="text-lg">{{ user.id }}</p>
            </div>
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">Username:</p>
              <p class="text-lg">{{ user.username }}</p>
            </div>
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">Email:</p>
              <p class="text-lg">{{ user.email }}</p>
            </div>
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">Admin:</p>
              <p class="text-lg">{{ user.is_admin ? 'yes' : 'no' }}</p>
            </div>
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">Created at:</p>
              <p class="text-lg">{{ user.created_at }}</p>
            </div>
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">Last Login at:</p>
              <p class="text-lg">{{ user.last_login_at ? user.last_login_at:'-' }}</p>
            </div>
            <div class="mb-4">
              <p class="mb-1 block text-teal-400">Token Valid after:</p>
              <p class="text-lg">{{ user.token_valid_after ? user.token_valid_after:'-' }}</p>
            </div>
          </div>
          <div v-else>
            <LoaderIcon class="size-8 mx-auto animate-spin text-teal-400 mt-10"/>
          </div>
      </div>


    </div>

  </adminWrapper>

</template>