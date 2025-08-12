<script setup>
  import { onMounted, ref, computed, watch, reactive } from 'vue'
  import apiClient from '@/api'
  import axios from 'axios';

  import { useIntersectionObserver } from '@/composables/useIntersectionObserver'
  import { useAbortController } from '@/composables/useAbortController'
  import { useLoaderStore } from '@/stores/loader'

  import FurnitureCard from '@/components/FurnitureCard.vue'
  import Loader from '@/assets/icons/Loader.svg'
  import publicWrapper from '@/wrappers/publicWrapper.vue'
  import Pagination from '@/components/Pagination.vue'


  // ここで onMounted が先に登録され、このコンポーネントの onMounted よりも先に実行される。
  const { addTarget, startObservation, prepareForUpdate } = useIntersectionObserver({ delayInterval: 100 })
  const { getNewSignal } = useAbortController()
  const loader = useLoaderStore()

  const furnitures = ref(null)
  const errors = ref(null)


  // onMounted(async()=>{
  //   // これより前に、冒頭でインポートした composable の方の onMounted が先に実行される。
  //   try{
  //     await fetchData()
  //     startObservation()

  //   }catch(err){
  //     console.error(err)
  //     errors.value = 'Failed to fetch the data. Please reload again later.'
  //   }
  // })
  onMounted(async () => {
  try {
    await handleDataFetch();
  } catch (err) {
    console.error(err);
    errors.value = 'Failed to fetch the data. Please reload again later.';
  }
});

  const query = ref('')
  const sort = ref('updated_desc')
  const sortField = computed(()=>{ return sort.value.split('_')[0]})
  const sortOrder = computed(()=>{ return sort.value.split('_')[1]})
  const paginationInfo = reactive({
    currentPage: 1,
    totalPages: 1,
    totalItems: 0
  })

  let timer = null;
  // watchのコールバック関数の役割は、あくまでタイマーをセットするという同期的な処理だから asyncをつける必要はない。
  // watch([query, sort], ()=>{
  //   paginationInfo.currentPage = 1 // 1ページ目に戻す
  //   if (timer !== null){
  //     clearTimeout(timer)
  //     timer = null
  //   }
  //   timer = setTimeout(async()=>{
  //     // v-forの差分更新を回避し、ディレイタイムなどを完全にリフレッシュするためにここでいったん空にしている
  //     furnitures.value = []
  //     prepareForUpdate()
  //     await fetchData()
  //     startObservation()
  //   }, 500)
  // })

  // watch(() => paginationInfo.currentPage, async (newPage, oldPage) => {
  //   if (newPage !== oldPage) {
  //     await fetchData();
  //     // ページトップにスクロール（任意）
  //     window.scrollTo(0, 0);
  //   }
  // });

  watch([query, sort], () => {
    paginationInfo.currentPage = 1 // 検索時は1ページ目に戻す
    if (timer !== null){
      clearTimeout(timer)
    }
    // デバウンス処理の後、新しい関数を呼ぶだけ
    timer = setTimeout(handleDataFetch, 500)
  })

  // 2. ページ切り替え用のwatch
  watch(() => paginationInfo.currentPage, async (newPage, oldPage) => { // ① async を追加
  if (newPage !== oldPage) {
    try {
      await handleDataFetch(); // ② await を追加
      window.scrollTo(0, 0);
    } catch (err) {
      // もし handleDataFetch 内で予期せぬエラーが起きた場合、ここで捕捉できる
      console.error('An error occurred during page transition:', err);
      // ここでユーザーにエラー通知を出すなどの処理も可能
    }
  }
});


  async function handleDataFetch() {
  errors.value = ''
    // v-forの差分更新を回避し、ディレイタイムなどを完全にリフレッシュするためにここでいったん空にしている
  furnitures.value = []
  prepareForUpdate()

  await fetchData()

  await startObservation()
}

  async function fetchData(){
    errors.value = ''
    const params = {
      q: query.value,
      sort: sortField.value,
      order: sortOrder.value,
      page: paginationInfo.currentPage
    }
    try{
      const response = await apiClient.get(`/api/v1/furnitures`, {
        params: params,
        signal: getNewSignal()
      })
      if (response && response.data){

        furnitures.value = response.data.furnitures
        if (furnitures.value.length === 0){
          errors.value = 'There is no items found.'
        }
        console.log(furnitures.value)
        // ページネーション情報を更新
        paginationInfo.totalPages = response.data.total_pages
        paginationInfo.totalItems = response.data.total_items
        // paginationInfo.currentPage = response.data.current_page
      }
    }catch(err){
      if (axios.isCancel(err)) { //ここのエラー判定でaxiosが必要
        // リクエストがキャンセルされた場合は、エラーとして扱う必要はない
        console.log('A request has been cancelled by AbortController.')
      } else if (err.response && err.response.status === 404) {
        // 404エラーの場合は、ページが存在しないか結果が0件
        furnitures.value = []
        paginationInfo.totalPages = 1
        paginationInfo.totalItems = 0
        console.log('Page not found or no results.')
      }
      else{
        console.log(err)
        errors.value = 'Failed to fetch data. Please try it again later.'
      }
    }
  }


</script>

<template>
  <publicWrapper>

    <div class="mb-8 md:mb-10 flex justify-between items-center gap-3 md:gap-6 px-1">
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

  </publicWrapper>


</template>
