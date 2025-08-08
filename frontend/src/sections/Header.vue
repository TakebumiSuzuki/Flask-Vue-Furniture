<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useNotificationStore} from '@/stores/notification'
  import Logo from '@/assets/images/logo.svg'
  import UserIcon from '@/assets/icons/UserIcon.svg'
  import HomeIcon from '@/assets/icons/Home.svg'
  import InstagramIcon from '@/assets/icons/Instagram.svg'
  import FacebookIcon from '@/assets/icons/Facebook.svg'
  import TikTokIcon from '@/assets/icons/TikTok.svg'
  import LogoutIcon from '@/assets/icons/Logout.svg'
  import LoginIcon from '@/assets/icons/Login.svg'
  import RegisterIcon from '@/assets/icons/Register.svg'


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
          <RouterLink :to="{name: 'home'}">
            <Logo alt="logo" class="text-neutral-700 !w-60 md:!w-70 hover:scale-103 transition"/>
          </RouterLink>
        </div>


        <div
          class="text-neutral-50 font-medium md:hidden absolute top-0 left-0 w-50 h-screen backdrop-blur-xs bg-neutral-600/80 transition duration-300 ease-in-out text-lg  z-300"
          :class="showSidePane ? 'translate-x-0': '-translate-x-50'"
          @click="showSidePane = false"
        >
          <div class="flex flex-col items-start ml-12 gap-3 mt-20 pb-3">
            <RouterLink
              :to="{name: 'home'}"
              class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
            >
              <div class="flex items-center gap-2 justify-start">
                <HomeIcon class="size-5"/>
                Home
              </div>
            </RouterLink>

          </div>

          <div v-if="authStore.isAuthenticated" class="flex flex-col items-start ml-12 gap-3">

            <RouterLink
              :to="{name: 'users'}"
              class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
            >
              <div class="flex items-center gap-2 justify-start">
                <UserIcon class="size-5"/>
                User Info
              </div>
            </RouterLink>


            <button
              type="button"
              @click="handleLogout"
              class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
            >
              <div class="flex items-center gap-2 justify-start">
                <LogoutIcon class="size-5"/>
                Logout
              </div>
            </button>
          </div>

          <div v-else class="flex flex-col items-start ml-12 gap-3">
              <RouterLink
                :to="{name: 'login'} "
                class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
              >
                <div class="flex items-center gap-2 justify-start">
                  <LoginIcon class="size-5.5 -ml-0.5"/>
                  Login
                </div>
              </RouterLink>

              <RouterLink
                :to="{name: 'register'}"
                class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
              >
                <div class="flex items-center gap-2 justify-start">
                <RegisterIcon class="size-5"/>
                Signup
              </div>
              </RouterLink>
          </div>
          <div class="bg-neutral-400 h-[1px] w-[80%] mx-auto my-4"></div>
          <div class="flex flex-col items-start ml-12 gap-3">
            <a href="https://www.instagram.com/"
              class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
              target="_blank" rel="noopener noreferrer"
            >
              <div class="flex items-center gap-2 justify-start">
                <InstagramIcon class="size-5"/>
                Instagram
              </div>
            </a>

            <a href="https://www.tiktok.com/explore"
              class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
              target="_blank" rel="noopener noreferrer"
            >
              <div class="flex items-center gap-2 justify-start">
                <TikTokIcon class="size-5"/>
                TikTok
              </div>
            </a>

            <a href="https://www.facebook.com/"
              class="animated-underline hover:scale-105 transition duration-300 ease-in-out"
              target="_blank" rel="noopener noreferrer"
            >
              <div class="flex items-center gap-2 justify-start">
                <FacebookIcon class="size-5"/>
                Facebook
              </div>
            </a>

          </div>
        </div>


        <div class="font-semibold">

          <div class="max-md:hidden">
            <div v-if="authStore.isAuthenticated" class="flex items-center gap-6 mr-4">

              <RouterLink :to="{name: 'user-info'}"><UserIcon class="size-6.5 hover:scale-110 transition"/></RouterLink>

              <button type="button" @click="handleLogout" class="hover:cursor-pointer hover:scale-110 transition animated-underline  text-lg">Logout</button>
            </div>
            <div v-else class="flex items-center gap-8 mr-4">
                <RouterLink :to="{name: 'login'}" class="hover:scale-110 transition animated-underline  text-lg">Login</RouterLink>
                <RouterLink :to="{name: 'register'}"  class="hover:scale-110 transition animated-underline text-lg">Signup</RouterLink>
            </div>
          </div>

          <div class="md:hidden">
            <div class="relative size-7.5  mr-2 hover:cursor-pointer" @click="toggleSidePane">
              <div
                class="h-[2px] w-full absolute top-1/2 -translate-y-[calc(0.65rem+1px)] left-0 bg-neutral-700 transition duration-300 ease-in-out"
                :class="showSidePane ? 'rotate-405 !-translate-y-[1px]':''"
              ></div>
              <div
                class="h-[2px] w-full absolute top-1/2 -translate-y-[1px] left-0 bg-neutral-700  transition duration-300 ease-in-out"
                :class="showSidePane ? 'opacity-0':''"
                ></div>
              <div
                class="h-[2px] w-full absolute bottom-1/2 translate-y-[calc(0.65rem+1px)] left-0 bg-neutral-700 transition duration-300 ease-in-out"
                :class="showSidePane ? '-rotate-405 !translate-y-[1px]':''"
              ></div>
            </div>

          </div>
        </div>

      </div>

    </div>

  </header>
</template>