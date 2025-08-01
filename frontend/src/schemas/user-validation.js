// ここの z はオブジェクトであり、インポートの仕組み上、シングルトンのように振る舞う
import { z } from 'zod';

// This corresponds to the `validate_password` function in Pydantic.
const passwordValidation = z
  .string()
  .nonempty('Password is required.')
  .min(7, 'Password must be at least 7 characters long.')
  .refine((data) => /\d/.test(data), {
    message: 'Password must contain at least one number.',
    path: [], // この場合、このフィールド自体のエラーとして認識される。また、削除しても良い。
  })
  .refine((data) => /[@$!%*?&]/.test(data), {
    message: 'Password must contain at least one special character (@$!%*?&).',
    path: [],
  });


// オブジェクトに対してメソッドを「鎖（チェーン）」のようにつなげて呼び出す書き方をする。
// これは、メソッドが常に自分自身のオブジェクト（または新しいオブジェクト）を返すことで実現されている。
// z は、Zodライブラリのすべての機能（メソッドや型定義）をプロパティとして持つ、巨大な一つのオブジェクト。
// z.object(), z.string(), z.email()などはすべて z オブジェクトがプロパティとして持っているメソッドで、
// これらのメソッドの戻り値も、メソッドチェーンを可能にするための、新しい「Zodスキーマオブジェクト」
export const createUserSchema = z.object({
    username: z
      .string() //これはString型であることを要求する。空文字はOK
      .nonempty('Username is required.')
      .min(3, 'Username must be at least 3 characters long.')
      .max(50, 'Username must be at most 50 characters long.'),
    email: z
      .string()
      .nonempty('Username is required.')
      .email('Please enter a valid email address.'),
    password: passwordValidation,
    password_confirmation: z
      .string()
      .nonempty('Password confirmation is required.'),
  })
  .refine((data) => data.password === data.password_confirmation, {
    message: "Passwords do not match.",
    path: ["password_confirmation"], // このエラーはpassword_confirmationのエラーと分類される
  });



export const changeUsernameSchema = z.object({
  newUsername: z
    .string({
      required_error: 'New username is required.',
    })
    .min(3, { message: 'Username must be at least 3 characters long.' })
    .max(50, { message: 'Username must be at most 50 characters long.' }),
});


export const changePasswordSchema = z.object({
  old_password: z
    .string()
    .nonempty('Password is required.'),
  new_password: passwordValidation,
  password_confirmation: z
    .string()
    .nonempty('Password confirmation is required.'),
  })
  .refine((data) => data.new_password === data.password_confirmation, {
      message: "Passwords do not match.",
      path: ["password_confirmation"],
  })
  .refine((data) => data.old_password !== data.new_password, {
    message: "New password must be different from the old password.",
    path: ["new_password"],
  });