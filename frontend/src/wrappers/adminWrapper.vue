<script setup>

</script>

<template>

  <div class="py-8 md:py-16 max-w-[1200px] w-full mx-auto">

    <div class="flex flex-col items-center justify-start
      md:flex-row md:items-start md:justify-center gap-0">

      <div class="w-full md:w-[10%] flex flex-row items-end justify-center md:flex-col md:gap-3  md:pt-10 pb-4 max-md:divide-x-1">
        <div class="pr-4 md:pr-6">
          <RouterLink :to="{ name: 'users'}">
            <span class="">Users</span>
          </RouterLink>

        </div>
        <div class="max-md:pl-4 md:pr-6">
          <RouterLink :to="{ name: 'furnitures'}">
            <span class="">Furniture</span>
          </RouterLink>
        </div>
      </div>
      <div class="w-full md:w-[80%] ">
        <slot></slot>
      </div>

    </div>
  </div>

</template>