<script setup>
  import Main from '@/sections/Main.vue';
  import Footer from '@/sections/Footer.vue';

  import MainVisual from '@/assets/images/mainvisual.jpg'
</script>

<template>
  <div class="relative flex flex-col min-h-screen ">
    <div class="absolute inset-0">
			<img :src="MainVisual" alt="" class="object-cover w-full h-full object-top">
		</div>
    
    <Main/>

    <Footer class="z-100"/>

  </div>

</template>