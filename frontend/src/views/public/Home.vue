<script setup>
  import { onMounted, ref, computed, watch, reactive } from 'vue'
  import apiClient from '@/api'
  import axios from 'axios';

  import { useIntersectionObserver } from '@/composables/useIntersectionObserver'
  import { useAbortController } from '@/composables/useAbortController'
  import { useLoaderStore } from '@/stores/loader'

  import Pagination from '@/components/Pagination.vue'
  import FurnitureCard from '@/components/FurnitureCard.vue'
  import Loader from '@/assets/icons/Loader.svg'
  import PublicWrapper from '@/wrappers/PublicWrapper.vue'

  // ここで onMounted が先に登録され、このコンポーネントの onMounted よりも先に実行される。
  const { addTarget, startObservation, prepareForUpdate } = useIntersectionObserver({ delayInterval: 100 })
  const { getNewSignal } = useAbortController()
  const loader = useLoaderStore()

  const furnitures = ref(null)
  const errors = ref(null)
  const query = ref('')
  const sort = ref('updated_desc')
  const sortField = computed(()=>{ return sort.value.split('_')[0]})
  const sortOrder = computed(()=>{ return sort.value.split('_')[1]})
  const paginationInfo = reactive({
    currentPage: 1, //ここにwatchを立てて、Paginationコンポーネントからイベントのイベントを監視
    totalPages: 1,
    totalItems: 0
  })

  onMounted(async () => {
    try {
      await handleDataFetch();

    }catch(err){
      console.error(err);
      errors.value = 'Failed to fetch the data. Please reload again later.';
    }
  });

  let timer = null;
  watch(
    [query, sort],
    () => {
      paginationInfo.currentPage = 1 // 検索時は1ページ目に戻す
      if (timer !== null){
        clearTimeout(timer)
      }
      timer = setTimeout(handleDataFetch, 500)
    }
  )

  // reactive オブジェクトの特定のプロパティを監視する際にはこのような getter にする必要がある。
  watch(
    () => paginationInfo.currentPage,
    (newPage, oldPage) => {
      if (newPage !== oldPage) {
        try {
          handleDataFetch();
          window.scrollTo(0, 0);
        }catch(err){
          // もし handleDataFetch 内で予期せぬエラーが起きた場合、ここで捕捉できる
          console.error('An error occurred during page transition:', err);
          // ここでユーザーにエラー通知を出すなどの処理も可能
        }
      }
  });


  async function handleDataFetch() {
    try {
      errors.value = ''
      // v-forの差分更新を回避し、ディレイタイムなどを完全にリフレッシュするために必要
      furnitures.value = []

      prepareForUpdate()

      const data = await fetchData()

      // 受け取ったデータでUIの状態を更新する
      furnitures.value = data.furnitures
      if (furnitures.value.length === 0) {
        errors.value = 'There are no items found.'
      }
      await startObservation()

      // Paginationコンポーネントの状態を更新
      paginationInfo.totalPages = data.total_pages
      paginationInfo.totalItems = data.total_items

    }catch(err){
      if (axios.isCancel(err)) {
        console.log('A request has been cancelled by AbortController.')
        // キャンセルの場合はユーザーにエラーを見せる必要はない
      }else if (err.response && err.response.status === 404) {
        furnitures.value = []
        errors.value = 'Page not found or no results.'
        paginationInfo.totalPages = 1
        paginationInfo.totalItems = 0
      }else{
        // その他の予期せぬエラー
        console.error('An error occurred during data fetching process:', err);
        errors.value = 'Failed to fetch data. Please try again later.'
      }
    }
  }

async function fetchData(){
  const params = {
    q: query.value,
    sort: sortField.value,
    order: sortOrder.value,
    page: paginationInfo.currentPage
  }
  const response = await apiClient.get(`/api/v1/furnitures`, {
    params: params,
    signal: getNewSignal() // これはサーバーには送られず、内部的に使うだけ
  })

  return response.data
}

</script>



<template>
  <PublicWrapper>

    <div class="mb-4 md:mb-6 flex justify-between items-center gap-3 md:gap-6 px-1">
      <input type="search" v-model="query" class="!w-[40%] grow !border-neutral-500">
      <select v-model="sort" class="border py-2.5 px-3 rounded-md outline-none !border-neutral-500 shadow-sm focus:shadow-md">
        <option value="price_asc">Price: Low to High</option>
        <option value="price_desc">Price: High to Low</option>
        <option value="created_asc">Date Added: Oldest</option>
        <option value="created_desc">Date Added: Newest</option>
        <option value="updated_asc">Least Recently Updated</option>
        <option value="updated_desc">Recently Updated</option>
      </select>
    </div>

    <!-- 検索を始めた後も, furnitures変数には今までのデーターが残り続けるのでローダーを表示させるために先に書く -->
    <div v-if="loader.loading">
      <Loader class="animate-spin size-14 mt-30 text-teal-400 mx-auto"/>
    </div>

    <div v-else-if="furnitures && furnitures.length > 0">
      <p
        class="text-center text-neutral-600 pb-2 md:pb-4 fade-in-element-from-left"
        :ref="addTarget"
      >
        Total {{ paginationInfo.totalItems }} items
      </p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="(furniture) in furnitures"
          :key="furniture.id"
          :ref="addTarget"
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

      <Pagination
        :totalPages="paginationInfo.totalPages"
        :currentPage="paginationInfo.currentPage"
        @update:currentPage="paginationInfo.currentPage = $event"
      />

    </div>

    <div v-else class="text-center mt-30">
      {{ errors }}
    </div>

  </PublicWrapper>


</template>
