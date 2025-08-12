import { onMounted, ref, onUnmounted, nextTick } from 'vue'

// インスタンス化の時に options={ delayInterval: 100 }のようにすると、各要素に100msの時間差ができる
export function useIntersectionObserver(options = {}){
  const defaultOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1,
    intersectingClass: 'is-visible',
    delayInterval: 100
  }
  // 後から記述されたもの（options）が前のもの（defaultOptions）を上書きしする。
  const config = {
    ...defaultOptions,
    ...options,
  }

  let observer = null
  let elementId = 0
  const targetElements = ref([])

  const addTarget = (el)=>{
    if(el){
      el.dataset.elementId = elementId
      elementId++
      targetElements.value.push(el)
    }
  }

  const createObserver = ()=>{
    return new IntersectionObserver(
    (entries, observer)=>{
      entries.sort((a, b) => a.target.dataset.elementId - b.target.dataset.elementId).forEach((entry)=>{
        if (entry.isIntersecting){
          const delayTime = entry.target.dataset.elementId * config.delayInterval || 0
          setTimeout(()=>{
            entry.target.classList.add(config.intersectingClass)
          }, delayTime)
          observer.unobserve(entry.target)
        }
      })
    },
    config
    )
  }

  onMounted(() => {
    console.log('onMountedが呼ばれています')
    observer = createObserver()
  })

  const prepareForUpdate = () => {
    elementId = 0
    // 既存のobserver登録をクリーンアップ
    targetElements.value.forEach(el => {
      if (el && observer){
        el.classList.remove(config.intersectingClass)
        observer.unobserve(el)
      }
    })
    targetElements.value = []
  }

  const startObservation = async () => {
    await nextTick()
    targetElements.value.forEach(el => {
      if (el && observer) observer.observe(el)
    })
  }

  onUnmounted(() => {
    console.log('onUnMountedが呼ばれています')
    if (observer) {
      observer.disconnect()
    }
  })

  return {
    addTarget,
    startObservation,
    prepareForUpdate,
  }
}

