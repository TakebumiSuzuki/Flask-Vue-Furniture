<script setup>
  import { computed, onMounted, ref, nextTick ,onUnmounted, onUpdated } from 'vue'
  import apiClient from '@/api'
  import { useIntersectionObserver } from '@/composables/useIntersectionObserver'
  import { useLoaderStore } from '@/stores/loader'

  import { formatDate } from '@/utilities'
  import Loader from '@/assets/icons/Loader.svg'
  import publicWrapper from '@/wrappers/publicWrapper.vue'

  const { registerElement, observeElements } = useIntersectionObserver({ delayInterval: 100 })
  const loaderStore = useLoaderStore()

  const props = defineProps({
    id: { type: [String, Number], required: true }
  })
  const numericId = computed(()=> Number(props.id))

  const furniture = ref(null)
  const error = ref(null)

  const formattedUpdatedAt = computed(() => {
    return furniture.value?.updated_at
      ? formatDate(furniture.value.updated_at)
      : '-'
  })


  onMounted(async ()=>{
    error.value = null

    try{
      const { data } = await apiClient.get(`/api/v1/furnitures/${numericId.value}`)
      furniture.value = data

      observeElements()

    }catch(err){
      console.error(err)
      error.value = 'Failed to fetch data. Please try reload this page again later.'
    }

  })


</script>

<template>
  <publicWrapper>
    <div v-if="furniture">
      <h1
        class="text-4xl font-medium text-center mt-4 fade-in-element"
        :ref="registerElement"
      >
        {{ furniture.name }}
      </h1>

      <p
        v-if="furniture.updated_at"
        class="mt-10 md:mt-12 text-neutral-500 text-sm fade-in-element-from-left"
        :ref="registerElement"
      >
        <i>Updated: {{ formattedUpdatedAt }}</i>
      </p>

      <div class="mt-1.5">
        <div class="flex md:flex-row flex-col items-start justify-center gap-4 md:gap-10">

          <div class="w-full md:w-[50%] fade-in-element-from-left" :ref="registerElement">
            <img
              :src="furniture.image_url"
              :alt="`Product Image of ${furniture.name}`"
              class="w-full aspect-square object-contain object-center shadow-lg">
          </div>

          <div class="w-full md:w-[50%]">
            <div
              :ref="registerElement"
              class="fade-in-element"
            >
              {{ furniture.description }}
            </div>

            <div
              class="grid grid-cols-[20%_80%] mt-8 md:mt-14 fade-in-element" :ref="registerElement">
              <div class="font-medium">Color:</div> <div>{{ furniture.color }}</div>
              <div class="font-medium">Price:</div> <div> {{ furniture.price }} USD</div>
            </div>

          </div>
        </div>

      </div>
    </div>

    <div v-else-if="loaderStore.loading">
      <Loader class="mx-auto size-10 animate-spin text-teal-400 mt-20"/>
    </div>
    <div v-else class="text-center mt-20">{{ error }}</div>
  </publicWrapper>

</template>

