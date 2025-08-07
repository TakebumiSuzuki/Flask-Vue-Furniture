<script setup>
  import { computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth';
  import { useAlertStore } from '@/stores/alert'
  import { useNotificationStore } from '@/stores/notification';

  import authWrapper from '@/wrappers/authWrapper.vue';

  import UserIcon from '@/assets/icons/UserIcon.svg'
  import EmailIcon from '@/assets/icons/EmailIcon.svg'
  import CalendarIcon from '@/assets/icons/CalendarIcon.svg'

  import { formatDate } from '@/utilities'

  const authStore = useAuthStore()
  const user = computed(()=> authStore.user)
  const alertStore = useAlertStore()
  const router = useRouter()
  const notificationStore = useNotificationStore();



  const formattedDate = computed(() => {
    if (!authStore.user?.created_at) {
      return '';
    }
    return formatDate(authStore.user.created_at)
  });

  const handleDeleteUser = async()=>{
    const result = await alertStore.showAlert(
      'Are you sure to delete your account?',
      [{ text: 'Yes', value: true, style: 'primary' }, { text: 'Cancel', value: false, style: 'secondary' }]
    )
    if (result){
      try{
        await authStore.deleteUser()
        router.push({ name: 'login' })
        notificationStore.showNotification('You have logged out.', 'success');
      }catch(err){
        console.log('ユーザーデリート処理中のエラーでました')
      }
    }
  }

</script>

<template>
  <div>
    <authWrapper>

      <h1 class="text-4xl text-center pt-10 pb-8">User Info</h1>

      <div class="max-w-100 w-full mx-auto pb-20 ">
        <div class="space-y-6 px-4 mb-10">
          <dl>
            <dt class="text-sm flex items-center gap-2"><UserIcon class= "size-5"/>Username:</dt>
            <dd class="text-lg">{{ user?.username }}</dd>
          </dl>
          <dl>
            <dt class="text-sm flex items-center gap-2"><EmailIcon class="size-5"/>Email:</dt>
            <dd class="text-lg">{{ user?.email }}</dd>
          </dl>
          <dl>
            <dt class="text-sm flex items-center gap-2"><CalendarIcon class="size-5"/>Date Joined: </dt>
            <dd class="text-lg">{{ formattedDate }}</dd>
          </dl>
        </div>

        <div class="flex flex-col gap-4 ">
          <RouterLink
            :to="{ name: 'change-username' }"
            class="btn bg-gradient-to-br from-neutral-400/80 to-neutral-500/80"
          >
            Change Username
          </RouterLink>

          <RouterLink
            :to="{ name: 'change-password' }"
            class="btn bg-gradient-to-br from-neutral-400/80 to-neutral-500/80"
          >
            Change Password
          </RouterLink>

          <button
            type="button"
            class="btn bg-gradient-to-br from-pink-300/50 to-pink-500/60 hover:from-pink-300/90 hover:to-pink-500/90"
            @click="handleDeleteUser"
          >
            Delete Account
          </button>

        </div>

      </div>



    </authWrapper>
  </div>

</template>