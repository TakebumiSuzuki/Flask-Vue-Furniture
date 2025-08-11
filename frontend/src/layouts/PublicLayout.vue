<script setup>
  import Header from '@/sections/Header.vue';
  import Footer from '@/sections/Footer.vue';
  import Main from '@/sections/Main.vue';

  import { useAuthStore } from '@/stores/auth'
  const authStore = useAuthStore()
</script>

<template>
  <div class="flex flex-col min-h-screen h-[1px]">

    <Header/>
    <div v-if="authStore.isAdmin" class="ralative z-250 w-full text-center  bg-teal-500/80 py-0.5  text-white">
      You are logged in as admin. >> Go to
      <RouterLink :to="{'name': 'users'}">
        <span class="underline ">Admin Page</span>
      </RouterLink>
    </div>
    <Main class="bg-gradient-to-br from-neutral-300 via-neutral-200 to-neutral-100"/>

    <Footer/>

  </div>

</template>