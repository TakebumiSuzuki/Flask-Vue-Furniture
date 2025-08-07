<script setup>
  import Header from '@/sections/Header.vue'
  import Main from '@/sections/Main.vue';
  import Footer from '@/sections/Footer.vue';

  import MainVisual from '@/assets/images/mainvisual.jpg'
</script>

<template>
  <div class="relative flex flex-col min-h-screen ">
    <div class="absolute inset-0 z-100">
			<img :src="MainVisual" alt="" class="object-cover w-full h-full object-top">
		</div>

    <Header class="relative z-300"/>
    <Main class="relative z-200"/>

    <Footer class="z-300"/>

  </div>

</template>