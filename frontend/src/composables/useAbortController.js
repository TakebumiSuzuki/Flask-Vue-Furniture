
// AbortControllerは、インスタンスひとつにつき、ひとつのAbortSignalしか管理できません。
// そして、そのシグナルは一度abort()されると、二度と元の状態には戻りません。
// AbortController の設計思想は、「使い捨てのキャンセルスイッチ」のようなもの
// new AbortController() で、新しい「スイッチとそれに繋がった電線（signal）」のセットを1つ作る感じ
export function useAbortController(){

  let controller;

  function getNewSignal(){
    if (controller){
        controller.abort()
    }
    controller = new AbortController()
    return controller.signal
  }

  return { getNewSignal }
}


