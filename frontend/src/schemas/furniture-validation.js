import { z } from "zod";

// z.enum() を使って、特定の値のみを許可するスキーマを定義します。
export const furnitureColorSchema = z.enum([
  "natural",
  "brown",
  "white",
  "black",
  "gray",
]);

export const createFurnitureSchema = z.object({

  name: z.string().min(3).max(50),
  description: z.string().max(1000),
  color: furnitureColorSchema,
  // ZodにはDecimal型がないため、一度数値に変換した上でカスタムバリデーションを適用します。
  // .pipe()を使い、z.coerce.number()で数値型に変換してからバリデーションを行います。
  price: z.coerce
    .number()
    .nonnegative("Price should be more than 0.")
    .refine(
      (n) => {
        // 文字列に変換してチェックします。
        const s = String(n);
        const parts = s.split("."); //ここでコンマがない時にエラーにならないか。。
        const integerPart = parts[0];
        const decimalPart = parts[1] || "";

        // decimal_places=2 に対応 (小数点以下が2桁以内)
        if (decimalPart.length > 2) {
          return false;
        }

        // max_digits=10 に対応 (全体の有効数字が10桁以内)
        // 小数点を除いた全体の桁数でチェックします。
        const totalDigits = integerPart.length + decimalPart.length;
        if (totalDigits > 10) {
          return false;
        }
        return true;
      },
      {
        message: "Please enter a price with up to 10 digits, including up to 2 decimal places.",
      }
    ),

  featured: z.coerce.boolean(),
  stock: z.coerce.number().int().nonnegative(), // ge=0 (>= 0) に対応
  // image_url: 文字列型でURL形式であることを検証
  // image_url: z.string().url("有効なURLを入力してください。").nullable().optional(),
});
// z.string().url(): 値が存在する場合、それはURL形式の文字列でなければならない。
// .nullable(): nullという値も許容する。
// .optional(): undefinedという値も許容する（=キーが存在しなくてもよい）。

// createFurnitureSchemaの全てのフィールドをオプショナル（任意）にします。
// .partial() を使うことで、既存のスキーマの全てのフィールドを任意に設定した新しいスキーマを簡単に作成できます。
export const updateFurnitureSchema = createFurnitureSchema.partial();
