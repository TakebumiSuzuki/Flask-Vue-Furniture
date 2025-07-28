<script setup>
  import Logo from '@/assets/images/logo.svg'

</script>

<template>
  <header class="px-2 md:px-6 bg-red-300">
    <div class="py-8 max-w-[1200px] w-full mx-auto">
      <div class="flex items-center justify-between">
        <div>
          <Logo alt="logo" class="text-red-400" />
        </div>


        <div class="flex items-center gap-8 ">
          <p>ログイン</p>
          <p>サインアップ</p>
        </div>


        <div class="flex items-center gap-8 ">
          <p>ログアウト</p>
          <p>アドミン</p>
        </div>

      </div>
    </div>

  </header>
</template>