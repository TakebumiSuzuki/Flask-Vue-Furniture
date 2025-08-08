<script setup>
  import Header from '@/sections/Header.vue'
  import Main from '@/sections/Main.vue';
  import Footer from '@/sections/Footer.vue';

  import MainVisual from '@/assets/images/mainvisual.jpg'

  import { useAuthStore } from '@/stores/auth'
  const authStore = useAuthStore()
</script>

<template>
  <div class="relative flex flex-col min-h-screen ">
    <div class="absolute inset-0 z-100">
			<img :src="MainVisual" alt="" class="object-cover w-full h-full object-top">
		</div>

    <Header class="relative z-300"/>
    <div v-if="authStore.isAdmin" class="ralative z-250 w-full text-center bg-pink-600/70 py-0.5  text-white">
      You are logged in as admin. Go to Admin Page
    </div>
    <Main class="relative z-200"/>

    <Footer class="z-300"/>

  </div>

</template>