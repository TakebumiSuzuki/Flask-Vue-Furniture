import { reactive, ref } from 'vue';
import { useLoaderStore } from '@/stores/loader'

export function useFormValidation(formData, schema){

  const isFormValid = ref(false)
  const errors = reactive({})

  const validateForm = ()=>{
    const parsed_data = schema.safeParse(formData)

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
    formData[field] = e.target.value

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

  const validateOnSubmit = ()=>{
    Object.keys(errors).forEach(key => { errors[key] = '' });
    const result = validateForm(formData)

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
    if (err.error_code !== 'VALIDATION_ERROR'){
      errors.root = err['message'] || 'An unexpected error occurred.'
    }else{
      for (const field in err['errors_dic']){

        errors[field] = err['errors_dic'][field]
      }
    }
  }


  return {
    isFormValid,
    errors,
    onInput,
    onBlur,
    validateOnSubmit,
    handleServerErrors
  };
}