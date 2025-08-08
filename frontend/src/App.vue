<script setup>
  import Notification from '@/components/Notification.vue';
  import Alert from '@/components/Alert.vue';
</script>

<template >
  <Alert class="z-1100"/>
  <Notification class=" z-1000"/>
  <RouterView class="font-custom text-neutral-700" />

</template>

