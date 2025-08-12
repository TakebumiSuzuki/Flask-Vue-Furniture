<script setup>
  import { onMounted, ref } from 'vue'
  import apiClient from '@/api'
  import { useIntersectionObserver } from '@/composables/useIntersectionObserver'
  import { useLoaderStore } from '@/stores/loader'

  import FurnitureCard from '@/components/FurnitureCard.vue'
  import Loader from '@/assets/icons/Loader.svg'
  import publicWrapper from '@/wrappers/publicWrapper.vue'

  // ここで onMounted が先に登録され、このコンポーネントの onMounted よりも先に実行される。
  const { registerElement, observeElements } = useIntersectionObserver({ delayInterval: 150 })
  const loader = useLoaderStore()

  const furnitures = ref(null)

  const error = ref(null)


  // 初回レンダリング（マウントフェーズ）。ここでは onBeforeUpdate と onUpdated は呼ばれない。
  // setup() → onBeforeMount → render → DOM作成 → onMounted
  // 2回目以降の変更（更新フェーズ）
  // リアクティブデータ変更 → onBeforeUpdate → re-render → DOM更新 → onUpdated
  onMounted(async()=>{
    // これより前に、冒頭でインポートした composable の方の onMounted が先に実行される。
    try{
      const response = await apiClient.get('/api/v1/furnitures')
      if (response && response.data){
        console.log(response.data)
        furnitures.value = response.data

        observeElements()
      }
    }catch(err){
      console.error(err)
      error.value = 'Failed to fetch the data. Please reload again later.'
    }
  })


</script>

<template>
  <publicWrapper>

    <div v-if="furnitures">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="(furniture) in furnitures"
          :key="furniture.id"
          :ref="registerElement"
          class="fade-in-element"
        >
          <RouterLink
            :to="{ name: 'home-furniture', params: {id: furniture.id}}"
          >
            <FurnitureCard
              :furniture = furniture
              class="hover:opacity-70 transition duration-300 ease-in-out hover:scale-103"
            />
          </RouterLink>
        </div>
      </div>
    </div>

    <div v-else-if="loader.loading">
      <Loader class="animate-spin size-14 mt-30 text-teal-400 mx-auto"/>
    </div>

    <div v-else class="text-center mt-30">
      {{ error }}
    </div>

  </publicWrapper>


</template>

