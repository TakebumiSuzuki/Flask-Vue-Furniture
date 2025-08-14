import { ref, computed } from 'vue'
import { defineStore } from "pinia";

export const useLoaderStore = defineStore('loader', ()=>{

    const loadingCount = ref(0)

    const loading = computed(()=>{ return loadingCount.value > 0 })


    const increaseCount = () => {
        console.log('loader increase called')
        loadingCount.value ++
    }

    const decreaseCount = () => {
        console.log('loader decrese called')
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