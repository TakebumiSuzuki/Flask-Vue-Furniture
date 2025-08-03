<script setup>
  import Notification from '@/components/Notification.vue';
  import Alert from '@/components/Alert.vue';
</script>

<template >
  <Alert/>
  <Notification/>
  <RouterView class="font-custom text-neutral-700" />

</template>

