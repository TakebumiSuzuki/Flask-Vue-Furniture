<script setup>
  import { reactive, computed, ref, watch, onUnmounted, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios' //Cloudinaryへのリクエストで使う
  import apiClient from '@/api'

  import { useNotificationStore } from '@/stores/notification';

  import { updateFurnitureSchema } from '@/schemas/furniture-validation.js'
  import { useFormValidation } from '@/composables/userFormValidation'
  import { validateImage } from '@/utilities'

  import CloseIcon from '@/assets/icons/Close.svg'
  import Check from '@/assets/icons/Check.svg'
  import Loader from '@/assets/icons/Loader.svg'

  import AdminWrapper from '@/wrappers/adminWrapper.vue'

  import { formatDate } from '@/utilities'


  const router = useRouter()
  const notificationStore = useNotificationStore();

  const isLoading = ref(false)

  const selectedFile = ref(null)
  const image_url = ref(null)
  const imageFileError = ref(null)
  // テンプレート中の ref="fileInput" と一致する名前の変数を用意すると、Vue がマウント時に fileInput.value に
  // DOM ノードを代入してくれる。imageのinputとselectedFileがv-modelでつながっていないためこれが必要。
  const fileInput = ref(null)
  let originalData



  const props = defineProps({id: { type: [String, Number], required: true}})
  const numericId = computed(() => {
    // Number()で数値に変換する
    return Number(props.id);
});

  const formData = reactive({
    name: '',
    description: '',
    color: 'white',
    price: '',
    featured: false,
    stock: 0,
  })

  const updates = reactive({})
  const haveUpdates = computed(()=>{
    return (Object.keys(updates).length !== 0)
  })

  watch([formData, image_url], (newValues, oldValues)=>{
    Object.keys(updates).forEach(key => delete updates[key]);

    const newFormData = newValues[0];
    const newImageUrl = newValues[1];
    console.log(`newFormData`, newFormData)
    console.log(`newImageUrl`, newImageUrl)

    Object.keys(newFormData).forEach((field) => {
      if (originalData.hasOwnProperty(field) && originalData[field] !== newFormData[field]){
        updates[field] = newFormData[field]
      }
    })
    if (originalData.hasOwnProperty('image_url') && originalData['image_url'] !== newImageUrl){
      updates.image_url = newImageUrl
    }
    console.log(`UPDATES `, updates)
  })

  const isButtonDisabled = computed(()=>{
    return (!isFormValid.value || isLoading.value || !haveUpdates.value)
  })


  const {
    validateForm,
    isFormValid,
    errors,
    onInput,
    onBlur,
    validateOnSubmit,
    handleServerErrors,
  } = useFormValidation(formData, updateFurnitureSchema)

  const createdAt = ref(null)
  const formatedCreatedAt = computed(()=>{ return formatDate(createdAt.value)})
  const updatedAt = ref(null)
  const formatedupdatedAt = computed(()=>{ return formatDate(updatedAt.value)})

  onMounted(async ()=>{
    try{
      const response = await apiClient.get(`/api/v1/admin/furnitures/${numericId.value}`)

      formData['name'] = response.data['name']
      formData['description'] = response.data['description']
      formData['color'] = response.data['color']
      const numValue = parseFloat(response.data['price']);
      formData['price'] = isNaN(numValue) ? '' : numValue;
      formData['featured'] = response.data['featured']
      formData['stock'] = response.data['stock']

      updatedAt.value = response.data['updated_at']
      createdAt.value = response.data['created_at']
      console.log(updatedAt.value)

      originalData = { ...formData };

      if (response.data.image_url){
        image_url.value = response.data.image_url
      }
      originalData.image_url = response.data.image_url
      console.log(`ORIGINAL`, originalData)
    }catch(err){
      console.log(err)
    }
  })

  const clearImageVariables = ()=>{
    selectedFile.value = null
    image_url.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }

  const onImageSelected = (e)=>{
    imageFileError.value = null
    if (e.target.files && e.target.files.length > 0){
      selectedFile.value = e.target.files[0]
      const error = validateImage(selectedFile.value)
      if (error){
        imageFileError.value = error
        clearImageVariables()
        return
      }
      image_url.value = URL.createObjectURL(selectedFile.value)
      const result = validateForm(formData)
      if (result){
          isFormValid.value = true
      }

    } else {
      imageFileError.value = 'Select a valid image.'
      clearImageVariables()
    }
  }

  // 重要：メモリリークを防ぐための後処理
  // imageUrlの値が変更されるたびに、古いURLを解放する
  watch(image_url, (newUrl, oldUrl) => {
    if (oldUrl) {
      URL.revokeObjectURL(oldUrl)
    }
  })
  onUnmounted(() => {
    if (image_url.value) {
      URL.revokeObjectURL(image_url.value)
    }
  })
  const onDeleteImage = ()=>{
    const result = validateForm(formData)
      if (result){
          isFormValid.value = true
      }
    clearImageVariables()
  }

  const uploadImage = async () => {

    const imageForm = new FormData();
    imageForm.append('file', selectedFile.value);
    // upload_preset  は CloudinaryのAPIが定義している、決まったキー名
    imageForm.append('upload_preset', 'furniture_unsigned');
    const url = `https://api.cloudinary.com/v1_1/deggnesko/image/upload`;
    try {
      const response = await axios.post(url, imageForm);
      return {
        secure_url: response.data.secure_url,
        delete_token: response.data.delete_token
      };

    } catch (err) {
      throw err
    }
  };

  const deleteImageFromCloudinary = async (deleteToken) => {
    console.log(`保存が失敗したのですでにアップロードしてしまった画像を消去しています...`);
    try {
      const url = `https://api.cloudinary.com/v1_1/deggnesko/delete_by_token`;
      await axios.post(url, { token: deleteToken });
      console.log(`Successfully deleted image from Cloudinary.`);

    } catch (err) {
      // ユーザーに直接見せる必要はないエラーなので、コンソールに出力する
      console.error('Failed to delete image from Cloudinary. This may require manual cleanup.', {
        error: err.response?.data || err.message,
      });
    }
  }

  async function onSubmit() {

    if (!haveUpdates){ return }

    const cleanedData = validateOnSubmit(updates)
    if (!cleanedData){ return }
    console.log('クリーンデータ(写真は除く):', cleanedData)

    isLoading.value = true
    let uploadedDeleteToken = null;

    if (selectedFile.value){
      try{
        const { secure_url, delete_token } = await uploadImage();
        image_url.value = secure_url
        uploadedDeleteToken = delete_token;
        imageFileError.value = null
        console.log('イメージアップロード成功:', secure_url);

      }catch(err){
        console.error(err)
        const message = err.response?.data?.error?.message || err.message || 'Failed to upload image.'
        imageFileError.value = message
        notificationStore.showNotification('Could not add the item because the image upload failed.', 'error');
        isLoading.value = false
        return
      }
    }

    try {
      cleanedData.image_url = image_url.value
      console.log(`ここが最終データーです`, cleanedData)
      await apiClient.patch(`/api/v1/admin/furnitures/${numericId.value}`, cleanedData)
      notificationStore.showNotification('New item was added!', 'success');
      router.push({name: 'furnitures'})
    } catch (err) {
      console.error(err)
      handleServerErrors(err)
      notificationStore.showNotification('Failed to save the new item. Please try it again later.', 'error');
      if (uploadedDeleteToken) {
        await deleteImageFromCloudinary(uploadedDeleteToken);
      }

    }finally{
      isLoading.value = false
    }
  }
</script>




<template>
  <AdminWrapper>
    <div class="px-2 md:px-4 md:border-l min-h-180 border-neutral-500">
      <h1 class="text-center text-4xl tracking-widest ">Edit Furniture</h1>

      <form @submit.prevent="onSubmit" class="max-w-[600px] w-full mx-auto mt-8 pb-24" novalidate>

        <RouterLink :to="{name: 'furnitures'}">
          <div class="text-neutral-300 size-fit px-0.5 animated-underline">
            &laquo; Go Back
          </div>
        </RouterLink>

        <div class="flex flex-col items-end mb-6 text-neutral-300 gap-0.5 text-sm">
          <div>Created: {{ formatedCreatedAt }}</div>
          <div>Last Update: {{ formatedupdatedAt }}</div>
        </div>

        <p class="validation-error-text !text-center break-words">{{ errors.root || '\u00A0' }}</p>

        <div class="mb-4">
          <label for="name" class="mb-1 block text-teal-400">Product Name</label>
          <input
            type="text"
            id="name"
            class="mb-1"
            :class="{ 'border-red-400': errors.name }"
            :value="formData.name"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
          <p class="validation-error-text !text-right break-words">{{ errors.name || '\u00A0' }}</p>
        </div>


        <div class="mb-4">
          <label for="description" class="mb-1 block text-teal-400">Description</label>
          <textarea
            id="description"
            rows="4"
            class="block px-4 py-2 border rounded-md outline-none shadow-sm focus:shadow-md w-full mb-1"
            :class="{ 'border-red-400': errors.description }"
            :value="formData.description"
            @input="onInput($event)"
            @blur="onBlur($event)"
          ></textarea>
          <p class="validation-error-text !text-right">{{ errors.description || '\u00A0' }}</p>

        </div>

        <div class="mb-4">
          <label for="color" class="mb-1 block text-teal-400">Color</label>
          <select
            id="color"
            class="mb-1 block px-4 py-2 border rounded-md outline-none shadow-sm focus:shadow-md w-40"
            :class="{ 'border-red-400': errors.color }"
            :value="formData.color"
            @change="onInput($event)"
            @blur="onBlur($event)"
          >
            <option value="natural">Natural</option>
            <option value="brown">Brown</option>
            <option value="white">White</option>
            <option value="black">Black</option>
            <option value="gray">Gray</option>
          </select>
          <p class="validation-error-text !text-left">{{ errors.color || '\u00A0' }}</p>

        </div>

        <div class="mb-4">
          <label for="price" class="mb-1 block text-teal-400">Price</label>
          <input
            type="number"
            id="price"
            step="0.01"
            min="0"
            inputmode="decimal"
            class="!w-40 mb-1"
            :class="{ 'border-red-400': errors.price }"
            :value="formData.price"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
          <p class="validation-error-text !text-left">{{ errors.price || '\u00A0' }}</p>
        </div>

        <div class="mb-4">
          <div class="flex justify-start items-center gap-4 mb-1">
            <label for="featured" class="text-teal-400">Featured</label>
            <input
              type="checkbox"
              id="featured"
              class="!w-5 size-4.5 accent-teal-600"
              :class="{ 'border-red-400': errors.featured }"
              :checked="formData.featured"
              @change="onInput($event)"
              @blur="onBlur($event)"
            >
          </div>
          <p class="validation-error-text !text-left">{{ errors.featured || '\u00A0' }}</p>
        </div>

        <div class="mb-4">
          <label for="stock" class="mb-1 block text-teal-400">Stock</label>
          <input
            type="number"
            id="stock"
            min="0"
            step="1"
            inputmode="numeric"
            class="mb-1 !w-40"
            :class="{ 'border-red-400': errors.stock }"
            :value="formData.stock"
            @input="onInput($event)"
            @blur="onBlur($event)"
          >
          <p class="validation-error-text !text-left">{{ errors.stock || '\u00A0' }}</p>
        </div>

<!--  -->
        <div class="mb-4">
          <label for="image" class="mb-1 block text-teal-400">Image</label>
          <input
            type="file"
            accept="image/*"
            id="image"
            ref="fileInput"
            class="sr-only"
            @change="onImageSelected($event)"
          >
          <div>
            <label
              for="image"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
              v-text="image_url ? 'Change Picture':'Select Picture'"
            ></label>
            <p class="validation-error-text !text-left mt-1 break-words">{{ imageFileError || '\u00A0' }}</p>
          </div>
          <div v-if="image_url" class="mt-3 mb-3 relative w-[70%]">
            <img :src="image_url" alt="Selected image" class=" aspect-auto object-contain object-center rounded-sm overflow-clip" >
            <CloseIcon
              class="absolute top-2 right-2 size-6 bg-neutral-700/80 rounded-full hover:cursor-pointer hover:scale-110 transition"
              @click="onDeleteImage"
            >
            </CloseIcon>
          </div>
        </div>


        <button
          type="submit"
          class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400 mt-12
            disabled:!cursor-not-allowed disabled:!from-neutral-400 disabled:!to-neutral-500 disabled:!scale-100
          "
          :disabled="isButtonDisabled"
        >
          <div v-if="isLoading" class="flex items-center gap-2 justify-center">
            <Loader class="animate-spin size-6 text-neutral-50"/>
            Processing
          </div>
          <div v-else class="flex items-center gap-2 justify-center">
            <Check class="size-5"/>
            Add Item
          </div>
        </button>

      </form>
    </div>

  </AdminWrapper>

</template>