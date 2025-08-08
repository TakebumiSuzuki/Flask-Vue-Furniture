<script setup>
  import { onMounted, ref } from 'vue'
  import apiClient from '@/api'
  import adminWrapper from '@/wrappers/adminWrapper.vue'
  import CheckIcon from '@/assets/icons/Check.svg'
  import PlusIcon from '@/assets/icons/Plus.svg'
  import LoaderIcon from '@/assets/icons/Loader.svg'
  import { useLoaderStore } from '@/stores/loader'

  const furnitures = ref(null)
  const loader = useLoaderStore()

  onMounted(async ()=>{
    try{
      const response = await apiClient.get('/api/v1/admin/furnitures')
      furnitures.value = response.data

    }catch(err){
      console.error(err)
    }
  })

</script>

<template>
  <adminWrapper>
    <div class="px-2 md:px-4 md:border-l min-h-180 border-neutral-500">
      <h1 class="text-center text-4xl tracking-widest mb-8">Furnitures</h1>

      <div class="flex justify-between items-center mb-10 px-2">

        <input type="search" placeholder="Search..." class="md:!w-[60%] !border-neutral-500">

        <RouterLink :to="{name:'furnitures-create'}">
          <div class="bg-gradient-to-br from-teal-800/80 to-teal-500/80   max-md:hidden px-10 py-2.5 rounded-md hover:scale-105 active:scale-103 transition ease-in-out flex items-center gap-1">
            <PlusIcon class="inline size-5"/>Add Item
          </div>
        </RouterLink>

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

        <div class="">
          <div v-for="furniture in furnitures" :key="furniture.id">
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
          <div v-for="furniture in furnitures" :key="furniture.id">
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

    </div>

    <RouterLink
      :to="{name:'furnitures-create'}"
      class="fixed bottom-6 right-6 rounded-full size-18 md:size-20 bg-gradient-to-br from-teal-700/80 to-teal-500/80 hover:cursor-pointer hover:scale-110 transition duration-200 ease-in-out hover:shadow-md flex justify-center items-center md:hidden active:scale-105"
    >
      <PlusIcon class="size-14 text-neutral-50/70"/>
    </RouterLink>

  </adminWrapper>

</template>