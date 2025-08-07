<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useNotificationStore} from '@/stores/notification'
  import Logo from '@/assets/images/logo.svg'

  const authStore = useAuthStore()
  const notificationStore = useNotificationStore()
  const router = useRouter()
  const showSidePane = ref(false)

  const toggleSidePane = ()=>{
    showSidePane.value = !showSidePane.value
    console.log(showSidePane.value)
  }

  const handleLogout = async()=>{
    try{
      await authStore.logout()
      router.push({name: 'home'})
      notificationStore.showNotification('You have logged out.', 'success');
    }catch(err){
      console.log(err)
      notificationStore.showNotification('Failed to logout try it later again.', 'error')

    }
  }

</script>

<template>
  <header class="relative px-4 md:px-8 bg-neutral-50 shadow-lg">
    <div class="py-6 max-w-[1200px] w-full mx-auto ">
      <div class="flex items-center justify-between">
        <div>
          <Logo alt="logo" class="text-neutral-700 !w-60 md:!w-70 "/>
        </div>


        <div class="md:hidden absolute top-0 left-0 w-40 h-screen backdrop-blur-xs bg-neutral-200/70 transition duration-300 ease-in-out text-lg"
          :class="showSidePane ? 'translate-x-0': '-translate-x-40'"
        >
          <div v-if="authStore.isAuthenticated" class="flex flex-col items-center gap-3 mt-20">
            <div v-if="authStore.isAdmin">
              <RouterLink
                :to="{name: 'users'}"
                class="hover:underline hover:underline-offset-4"
              >
                Admin
              </RouterLink>
            </div>

            <button
              type="button"
              @click="handleLogout"
              class="hover:underline hover:underline-offset-4"
            >
              Logout
            </button>
          </div>

          <div v-else class="flex flex-col items-center gap-3  mt-20">
              <RouterLink
                :to="{name: 'login'} "
                class="hover:underline hover:underline-offset-4"
              >
                LOGIN
              </RouterLink>

              <RouterLink
                :to="{name: 'register'}"
                class="hover:underline hover:underline-offset-4"
              >
                SIGNUP
              </RouterLink>
          </div>
        </div>


        <div class="font-medium">

          <div class="max-md:hidden">
            <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
              <div v-if="authStore.isAdmin">
                <RouterLink :to="{name: 'users'}">Admin</RouterLink>
              </div>
              <button type="button" @click="handleLogout" class="hover:cursor-pointer">Logout</button>
            </div>
            <div v-else class="flex items-center gap-8">
                <RouterLink :to="{name: 'login'}">LogIn</RouterLink>
                <RouterLink :to="{name: 'register'}">SignUp</RouterLink>
            </div>
          </div>

          <div class="md:hidden">
            <div class="relative size-7.5  mr-2 hover:cursor-pointer" @click="toggleSidePane">
              <div
                class="h-[2px] w-full absolute top-0 translate-y-[3px] left-0 bg-neutral-700 transition duration-500 ease-in-out"
                :class="showSidePane ? 'rotate-405 !translate-y-[calc(3.75rm-1px)]':''"
              ></div>
              <div class="h-[2px] w-full absolute top-1/2 -translate-y-[1px] left-0 bg-neutral-700"></div>
              <div class="h-[2px] w-full absolute bottom-0 -translate-y-[3px] left-0 bg-neutral-700"></div>
            </div>

          </div>
        </div>

      </div>

    </div>

  </header>
</template>