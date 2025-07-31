<script setup>
  import { computed } from 'vue'
  import { useAuthStore } from '@/stores/auth';

  const authStore = useAuthStore()
  const user = computed(()=> authStore.user)

</script>

<template>
  <div class="relative pt-[10%] max-w-[600px] w-full h-full mx-auto ">

    <div class="rounded-xl shadow-xl backdrop-blur-sm bg-white/60">

      <h1 class="text-4xl text-center py-8">User Info</h1>

      <p>Username:</p>
      <p>{{ user?.username }}</p>
      <p>Email:</p>
      <p>{{ user?.email }}</p>
      <p>Joined on:</p>
      <p>---</p>

    </div>

  </div>

</template>