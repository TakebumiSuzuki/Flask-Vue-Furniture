<script setup>
  import { onMounted, ref, reactive, watch, computed, onBeforeUnmount } from 'vue'
  import apiClient from '@/api'
  import axios from 'axios';
  import { useLoaderStore } from '@/stores/loader'
  import { useAbortController } from '@/composables/useAbortController'

  import CheckIcon from '@/assets/icons/Check.svg'
  import PlusIcon from '@/assets/icons/Plus.svg'
  import LoaderIcon from '@/assets/icons/Loader.svg'

  import Pagination from '@/components/Pagination.vue'
  import AdminWrapper from '@/wrappers/AdminWrapper.vue'

  const loader = useLoaderStore()
  const { getNewSignal } = useAbortController()

  const furnitures = ref([])
  const errors = reactive({})
  const query = ref('')
  const sort = ref('updated_desc')
  const sortField = computed(()=>{
    return sort.value.split('_')[0]
  })
  const sortOrder = computed(()=>{
    return sort.value.split('_')[1]
  })

  const paginationInfo = reactive({
    currentPage: 1,
    totalPages: 1,
    totalItems: 0
  })

  onMounted(async ()=>{
    await fetchData()
  })

  async function fetchData(){
    errors.search = ''
    const params = {
      q: query.value,
      sort: sortField.value,
      order:sortOrder.value,
      p: paginationInfo.currentPage
    }
    try{
      const response = await apiClient.get(`/api/v1/admin/furnitures`, {
        params: params,
        signal: getNewSignal()
      })
      if (response && response.data){
        console.log(response.data)
        furnitures.value = response.data.furnitures // 家具リストを更新
        // ページネーション情報を更新
        paginationInfo.totalPages = response.data.total_pages
        paginationInfo.totalItems = response.data.total_items
        paginationInfo.currentPage = response.data.current_page
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
        errors.search = 'Failed to fetch data. Please try it again later.'
      }
    }
  }

  let timer = null;
  watch([query, sort], ()=>{
    paginationInfo.currentPage = 1 // 1ページ目に戻す
    if (timer !== null){
      clearTimeout(timer)
      timer = null
    }
    timer = setTimeout(async()=>{
      await fetchData()}
      , 500)
  })

  watch(() => paginationInfo.currentPage, async (newPage, oldPage) => {
    if (newPage !== oldPage) {
      await fetchData();
      // ページトップにスクロール（任意）
      window.scrollTo(0, 0);
    }
  });

  onBeforeUnmount(()=>{
    if (timer !== null){
      clearTimeout(timer)
      timer = null
    }
  })


</script>

<template>
  <AdminWrapper>
    <div class="px-2 md:px-4 md:border-l min-h-180 border-neutral-500">
      <h1 class="text-center text-4xl tracking-widest mb-8">Furnitures</h1>

      <div class="flex md:justify-between items-end mb-10 px-2 gap-4">

        <div class="flex flex-col md:w-[30%] grow">
          <p class="validation-error-text pr-2">{{ errors.search || '\u00A0' }}</p>
          <input
            type="search" placeholder="Search..."
            class=" !border-neutral-500 block"
            v-model.trim="query"
          >
        </div>

        <div class="">
          <select
            name="orderQuery"
            class="px-3 py-2.5  border-1 rounded-md border-neutral-500 focus:outline-none"
            v-model="sort"
          >
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="stock_asc">Stock: Low to High</option>
            <option value="stock_desc">Stock: High to Low</option>
            <option value="created_asc">Date Added: Oldest</option>
            <option value="created_desc">Date Added: Newest</option>
            <option value="updated_asc">Least Recently Updated</option>
            <option value="updated_desc">Recently Updated</option>
          </select>
        </div>

        <div class="">
          <RouterLink :to="{name:'furnitures-create'}" >
            <div class="bg-gradient-to-br from-teal-800/80 to-teal-500/80  max-md:hidden px-4 py-2.5 rounded-md hover:scale-105 active:scale-103 transition ease-in-out flex items-center gap-1 justify-center">
              <PlusIcon class="inline size-5"/>Add Item
            </div>
          </RouterLink>
        </div>

      </div>


      <div class="max-md:hidden pb-16 md:px-2 rounded-lg text-sm md:text-base">
        <div class="md:px-4 grid md:grid-cols-[4%_50px_auto_12%_12%_8%_9%] items-center md:gap-6 text-left border-b-2 pb-1 border-neutral-500 text-teal-400">
              <p class="text-center">ID</p>
              <p class="text-center">Image</p>
              <p class="">Name</p>
              <p class="text-center">Color</p>
              <p class="text-center">Price</p>
              <p class="text-center">Stock</p>
              <p class="text-center">Featured</p>
        </div>

        <div v-if="!loader.loading">
          <div v-if="furnitures.length === 0" class="text-center">There is no results found.</div>
          <div v-else v-for="furniture in furnitures" :key="furniture.id">
            <RouterLink :to="{ name: 'furnitures-update', params: { id: furniture.id }}">
              <div class="md:px-4 grid md:grid-cols-[4%_50px_auto_12%_12%_8%_9%] items-center md:gap-6 text-left  border-neutral-500 text-neutral-50 border-dotted border-b py-1 hover:bg-neutral-600 transition ease-in-out duration-300">
                <p class="text-center">{{furniture.id}}</p>
                <img :src="furniture.image_url" alt="Product Image" class="object-contain aspect-auto block h-[50px] w-full">
                <p class="truncate">{{ furniture.name }}</p>
                <p class="truncate text-center">{{ furniture.color }}</p>
                <p class="truncate text-right">{{ furniture.price }}</p>
                <p class="text-center">{{ furniture.stock }}</p>
                <div class="flex justify-center items-center">
                  <div v-if="furniture.featured" class="size-5 text-teal-400"><CheckIcon/></div>
                  <div v-else>-</div>
                </div>
              </div>
            </RouterLink>
          </div>

        </div>
      </div>

      <div v-if="!loader.loading">
        <div class="md:hidden">
          <div v-if="furnitures.length === 0" class="text-center">There is no reults found.</div>
          <div v-else v-for="furniture in furnitures" :key="furniture.id">
            <RouterLink :to="{ name: 'furnitures-update', params: { id: furniture.id }}">
              <div class="flex items-start gap-4 sm:gap-6 py-4 border-dotted border-b border-neutral-500  sm:px-4 px-2 hover:bg-neutral-600 transition ease-in-out duration-300">
                <div class="w-1/2">
                  <img
                  :src="furniture.image_url"
                  alt="Product Image"
                  class="w-full aspect-square object-cover object-center"
                  >
                </div>
                <div class="w-1/2 space-y-2 sm:mt-6">
                  <p class="truncate max-sm:text-sm text-right">ID: {{ furniture.id }}</p>
                  <p class="sm:text-lg text-right truncate">{{ furniture.name }}</p>
                  <div class="flex justify-between items-center max-sm:text-sm">
                    <span class="text-teal-400">Color:</span>
                    {{ furniture.color }}
                  </div>
                  <div class="flex justify-between items-center max-sm:text-sm">
                    <span class="text-teal-400">Price:</span>
                    {{ furniture.price }}
                  </div>
                  <div class="flex justify-between items-center max-sm:text-sm">
                    <span class="text-teal-400">Stock:</span>
                    {{ furniture.stock }}
                  </div>
                  <div class="flex justify-between items-center max-sm:text-sm">
                    <span class="text-teal-400">Featured:</span>
                    <div class="flex justify-center items-center">
                      <div v-if="furniture.featured" class="size-5"><CheckIcon/></div>
                      <div v-else>-</div>
                    </div>
                  </div>
                </div>

              </div>
            </RouterLink>


          </div>

        </div>
      </div>

      <div v-else>
        <LoaderIcon class="animate-spin size-10 block mx-auto  text-teal-400/70"/>
      </div>

      <div v-if="!loader.loading && furnitures.length > 0">
        <Pagination
          :total-pages="paginationInfo.totalPages"
          :current-page="paginationInfo.currentPage"
          @update:currentPage="paginationInfo.currentPage = $event"
        />
        <p class="text-center text-sm text-neutral-400 mt-4 pb-10">
          Total {{ paginationInfo.totalItems }} items
        </p>
      </div>

    </div>

    <RouterLink
      :to="{name:'furnitures-create'}"
      class="fixed bottom-6 right-6 rounded-full size-18 md:size-20 bg-gradient-to-br from-teal-700/80 to-teal-500/80 hover:cursor-pointer hover:scale-110 transition duration-200 ease-in-out hover:shadow-md flex justify-center items-center md:hidden active:scale-105"
    >
      <PlusIcon class="size-14 text-neutral-50/70"/>
    </RouterLink>



  </AdminWrapper>

</template>