<script setup>

  const props = defineProps({
    furniture: Object,
    required: true
  })


</script>


<template>
  <div>
    <div class="relative">
      <img :src="furniture.image_url" alt="`Image for '${furniture.name}'`"
        class="w-full aspect-square object-cover object-center block"
      >
      <div class="absolute bottom-[2%] right-[2%] text-sm text-neutral-50 backdrop-blur-xs rounded px-1.5 py-0.5 bg-neutral-800/50">
        ${{ furniture.price }}
      </div>
    </div>
    <div class="flex flex-col justify-between text-sm">
      <p class="truncate">{{ furniture.name }}</p>
    </div>




  </div>


</template>