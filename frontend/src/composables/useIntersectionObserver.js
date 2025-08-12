import { onMounted, ref, onUnmounted, nextTick, onBeforeUpdate, onUpdated } from 'vue'

// インスタンス化の時に options={ delayInterval: 100 }のようにすると、各要素に100msの時間差ができる
export function useIntersectionObserver(options = {}){

  const fadeElements = ref([])
  let observer = null
  let delayMultiplier = 0

  const defaultOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1,
    className: 'is-visible'
  }

  // 後から記述されたもの（options）が前のもの（defaultOptions）を上書きしする。
  const config = {
    ...defaultOptions,
    ...options,
    delayInterval: options.delayInterval || 100
  }

  const registerElement = (el)=>{
    if(el){
      el.dataset.fadeDelay = delayMultiplier * config.delayInterval
      delayMultiplier++
      fadeElements.value.push(el)
    }
  }

  const createObserver = ()=>{
    return new IntersectionObserver(
    (entries, observer)=>{
      entries.forEach((entry)=>{
        if (entry.isIntersecting){
          const delayTime = entry.target.dataset.fadeDelay || 0
          setTimeout(()=>{
            entry.target.classList.add(config.className)
          }, delayTime)
          observer.unobserve(entry.target)
        }
      })
    },
    config
    )
  }

  // この関数は呼び出し元でも使う必要あり。
  const observeElements = async () => {
    await nextTick()
    fadeElements.value.forEach(el => {
      if (el && observer) observer.observe(el)
    })
  }

  onMounted(() => {
    observer = createObserver()
  })

  // これらonBeforeUpdateとonUpdatedはonMountedとは一緒には呼ばれない。
  // onMounted後にリアクティブな値がアップデートされ、再レンダリングするときに呼ばれる。　
  onBeforeUpdate(() => {
    delayMultiplier = 0
    // 既存のobserver登録をクリーンアップ
    fadeElements.value.forEach(el => {
      if (el && observer) observer.unobserve(el)
    })
    fadeElements.value = []
  })

  onUpdated(()=>{
    observeElements()
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
    }
  })

  return {
    registerElement,
    observeElements,
  }
}

