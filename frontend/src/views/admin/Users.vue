<script setup>
  import { onMounted, ref } from 'vue'
  import apiClient from '@/api'
  import { useRouter } from 'vue-router'

  import { useAuthStore} from '@/stores/auth'
  import { useNotificationStore} from '@/stores/notification'
  import { useAlertStore } from '@/stores/alert'

  import adminWrapper from '@/wrappers/adminWrapper.vue'
  import CheckIcon from '@/assets/icons/Check.svg'
  import DeleteIcon from '@/assets/icons/Delete.svg'

  const users = ref(null)

  const router = useRouter()
  const authStore = useAuthStore()
  const alertStore = useAlertStore()
  const notificationStore = useNotificationStore()

  const fetchUsers = async() =>{
    const result = await apiClient.get('/api/v1/admin/users')
    console.log(result.data)
    users.value = result.data.users
  }

  onMounted(async ()=>{
    try{
      await fetchUsers()
    }catch(err){
      console.log(err)
      notificationStore.showNotification('Failed to fetch data.', 'error')
    }
  })


  const handleDelete = async(user_id)=>{
    const result = await alertStore.showAlert(
      'Are you sure to delete this user?',
      [{ text: 'Yes', value: true, style: 'primary' }, { text: 'Cancel', value: false, style: 'secondary' }]
    )
    if (result){
      try{
        await authStore.deleteOtherUser(user_id)
        notificationStore.showNotification('Successfully the user has been deleted.', 'success');
        await fetchUsers()
      }catch(err){
        console.log(err)
        notificationStore.showNotification('Failed to delete user.', 'error');
      }
    }
  }

  const handleAdminChange = async(user_id)=>{
    try{
      await authStore.changeIsAdmin(user_id)
      notificationStore.showNotification("User's rols has been changed.", 'success');
      await fetchUsers()
    }catch(err){
      console.log(err)
      notificationStore.showNotification("Failed to change the user's role.", 'error');
    }
  }

</script>


<template>

  <adminWrapper>
    <div class="px-2 md:px-4 md:border-l">
      <h1 class="text-center text-4xl tracking-widest">All Users</h1>

      <div class="mt-12 pb-16 md:px-2 rounded-lg text-sm md:text-base">
        <div class="px-2 md:px-4 grid grid-cols-[auto_20%_30%_8%_5%] items-center gap-2 md:gap-8 text-left border-b-2 pb-1 border-neutral-400 text-teal-400">
          <p>ID</p>
          <p>Username</p>
          <p>Email</p>
          <p class="text-center">Admin</p>
          <p class="text-center"> </p>
        </div>

        <RouterLink
          v-for="user in users"
          :to="{ name: 'user-detail', params: { id: user.id }  }"
          class="py-3 px-2 md:px-4 text-sm md:text-base  border-neutral-400 border-dotted
          grid grid-cols-[auto_20%_30%_8%_5%] gap-2 md:gap-8 items-center text-center border-b  [&>p]:text-left
          hover:bg-neutral-600 transition duration-200 ease-in-out hover:cursor-pointer"
          :key="user.id"
        >
          <p class="truncate text-sm min-w-[50px]">{{user.id}}</p>
          <p class="truncate">{{user.username}}</p>
          <p class="truncate">{{user.email}}</p>
          <input
            type="checkbox"
            :checked="user.is_admin"
            @click.stop
            @change.prevent.stop="handleAdminChange(user.id)"
            class="accent-teal-400 size-4"
          >
          <button
            type="button"
            class="text-sm px-3 py-1 bg-gradient-to-br from-teal-400/80 to-teal-400/80 rounded-md mx-auto hover:scale-105 transition duration-200 ease-in-out hover:cursor-pointer"
            @click.prevent.stop="handleDelete(user.id)"
          >
            <!-- .preventによって<RouterLink>のデフォルト機能である画面遷移を止める。
              .stopによってバブルアップを止める-->
            <DeleteIcon class="size-4"/>
          </button>

        </RouterLink>
      </div>

    </div>

  </adminWrapper>

</template>