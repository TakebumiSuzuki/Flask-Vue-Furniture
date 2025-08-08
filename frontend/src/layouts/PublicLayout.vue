<script setup>
  import Header from '@/sections/Header.vue';
  import Footer from '@/sections/Footer.vue';
  import Main from '@/sections/Main.vue';

  import { useAuthStore } from '@/stores/auth'
  const authStore = useAuthStore()
</script>

<template>
  <div class="flex flex-col min-h-screen">

    <Header/>
    <div v-if="authStore.isAdmin" class="ralative z-250 w-full text-center bg-pink-700/50 py-0.5  text-white">
      You are logged in as admin. >> Go to
      <RouterLink :to="{'name': 'users'}">
        <span class="underline ">Admin Page</span>
      </RouterLink>
    </div>
    <Main/>
    <Footer/>

  </div>

</template>