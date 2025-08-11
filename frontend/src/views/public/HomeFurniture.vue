<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    id: String,
    required: true
  })
  const numericId = computed(()=> Number(props.id.value))

</script>

<template>
  test

</template>