<script setup>

</script>

<template>

  <div class="py-8 md:py-16 max-w-[1200px] w-full mx-auto ">

    <div class="flex flex-col items-center justify-start
      md:flex-row md:items-start md:justify-center gap-8">

      <div class="w-full md:w-[8%] flex flex-row items-center justify-center md:flex-col md:gap-2">

        <span class="px-6 max-md:border-r hover:cursor-pointer">Users</span>
        <span class="px-6 hover:cursor-pointer">Furniture</span>
      </div>
      <div class="w-full md:w-[80%]">
        <slot></slot>
      </div>

    </div>
  </div>

</template>