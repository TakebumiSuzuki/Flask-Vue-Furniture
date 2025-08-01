import { reactive, computed } from 'vue';

export function useFormValidation(){


  const onBlur = (e)=>{
    const key = e.target.id
    const result = validateForm(formData)
    if (result.errors?.[key]){
      errors[key] = result.errors[key] //そのフィールドを追跡モードに入れる
    }
  }

  return {
    onBlur
  }

}