import { reactive, ref } from 'vue';
import { useLoaderStore } from '@/stores/loader'

export function useFormValidation(formData, schema){

  const isFormValid = ref(false)
  const errors = reactive({})

  const validateForm = (data)=>{
    const parsed_data = schema.safeParse(data)

    if (parsed_data.success){
      return { cleanData: parsed_data.data, errors: null }

    }else{
      const new_errors = {}
      const { formErrors, fieldErrors } = parsed_data.error.flatten();
      if (formErrors.length > 0) {
        new_errors['root'] = formErrors[0];
      }
      for (const key in fieldErrors) {
        const messages = fieldErrors[key];
        if (messages) {
          new_errors[key] = messages[0];
        }
      }
      return { cleanData: null, errors: new_errors}
    }
  }

  const onInput = (e)=>{
    const field = e.target.id
    if (e.target.type === 'checkbox') {
      formData[field] = e.target.checked
    }else if (e.target.type === 'number') {
      // `value`が空文字列の場合も考慮し、数値にパースする
      const numValue = parseFloat(e.target.value);
      formData[field] = isNaN(numValue) ? '' : numValue; // 不正な入力の場合は空文字などを設定
      console.log(`Field: ${field}, Type: ${typeof formData[field]}, Value:`, formData[field]);
    }else{
      formData[field] = e.target.value
    }
    const result = validateForm(formData) // if節の中でなくここに書くのは、buttonのdisableのため
    isFormValid.value = Boolean(result.cleanData)

    if (field in errors){ //そのフィールドがすでに追跡モードに入っていた場合
      errors[field] = ''
      if (result.errors?.[field]){
        errors[field] = result.errors[field]
      }
    }
  }

  const onBlur = (e)=>{
    const field = e.target.id
    const result = validateForm(formData)
    if (result.errors?.[field]){
      errors[field] = result.errors[field] //そのフィールドを追跡モードに入れる
    }
  }

  const validateOnSubmit = (data)=>{
    Object.keys(errors).forEach(key => { errors[key] = '' });
    const result = validateForm(data)

    if (result.errors){
      for (const field in result.errors){
        errors[field] = result.errors[field]
      }
      return null
    }else{
      return result.cleanData
    }
  }

  const handleServerErrors = (err) =>{
    console.log(err.response)
    if (err.response && err.response.data) {
      const responseData = err.response.data;

      if (responseData && responseData.error_code === 'RESOURCE_CONFLICT'){
        errors.root = responseData.message

      }else if(responseData && responseData.error_code === 'VALIDATION_ERROR'){
        for (const field in responseData['errors_dic']){
          errors[field] = responseData['errors_dic'][field]
        }
      }
      else{
        errors.root = responseData['message'] || 'An unexpected error occurred.'
      }
    }
  }


  return {
    isFormValid,
    errors,
    onInput,
    onBlur,
    validateForm,
    validateOnSubmit,
    handleServerErrors
  };
}