import { ref, computed } from 'vue'
import { defineStore } from "pinia";

export const useLoaderStore = defineStore('loader', ()=>{

    const loadingCount = ref(0)

    const loading = computed(()=>{ loadingCount.value > 0 })


    const increaseCount = () => {
        loadingCount.value ++
    }

    const decreaseCount = () => {
        if (loadingCount.value > 0){
            loadingCount.value --
        }

    }

    return {
        loading,
        increaseCount,
        decreaseCount
    }
})