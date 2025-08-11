<script setup>
  import { onMounted, ref, onUnmounted, nextTick } from 'vue'
  import apiClient from '@/api'
  import { useLoaderStore } from '@/stores/loader'
  import publicWrapper from '@/wrappers/publicWrapper.vue'
  import FurnitureCard from '@/components/FurnitureCard.vue'

  const loader = useLoaderStore()
  const furnitures = ref(null)
  const cardElements = ref([])
  let observer = new IntersectionObserver(
    (entries, observer)=>{
      entries.forEach((entry)=>{
        if (entry.isIntersecting){
          entry.target.classList.add('is-visible')
          observer.unobserve(entry.target)
        }
      })
    },
    {
      root: null, // ビューポートを基準にする
      rootMargin: '0px',
      threshold: 0.1 // 要素が10%見えたらトリガー
    }
  )

  onMounted(async()=>{

    try{
      const response = await apiClient.get('/api/v1/furnitures')

      if (response && response.data){
        furnitures.value = response.data
        console.log(response.data)

        await nextTick()

        cardElements.value.forEach(el => {
          if (el) observer.observe(el)
        })
      }
    }catch(err){
      console.error(err)
    }
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
    }
  })

</script>

<template>
  <publicWrapper>
    <div v-if="furnitures">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="(furniture, index) in furnitures"
          :key="furniture.id"
          :ref="(el)=>{cardElements.push(el)}"
          class="fade-in-element"
          :style="{ transitionDelay: (index * 50) + 'ms' }"
        >
          <RouterLink :to="{ name: 'home-furniture', params: {id: furniture.id}}" :id="furniture.id">
            <FurnitureCard :furniture = furniture
              class="hover:opacity-70 transition duration-300 ease-in-out hover:scale-103"
            ></FurnitureCard>
          </RouterLink>
        </div>
      </div>

    </div>

  </publicWrapper>

</template>

<style scoped>
.fade-in-element {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}

/* 画面内に入ったときに適用される状態 */
.fade-in-element.is-visible {
  opacity: 1;
  transform: translateY(0);
}
</style>