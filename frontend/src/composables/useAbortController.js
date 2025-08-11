

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


