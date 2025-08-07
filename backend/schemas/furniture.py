from pydantic import BaseModel, Field, ConfigDict, HttpUrl, field_serializer
from typing import Annotated
from decimal import Decimal
from datetime import datetime
from enum import Enum


class FurnitureColor(str, Enum):
    NATURAL = "natural"
    BROWN = "brown"
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"

# クライアント側が image_url の入力フィールドが空の場合に、そのキー自体を送信データから除外して送ってきた場合、
# クライアント側が image_url の入力フィールドが空の場合に、JSONの null を明示的に送信してきた場合、
# どちらの場合も、Pydantic側では image_url は None として処理され、モデルには null で値が入る。
# しかし！！ updateのview関数で model_dump(exclude_unset=True)としているので、クライアント側は、
# 写真を削除する意思がある時には、明示的に nullとし、逆に写真をいじらない場合には
# image_urlをキーに含めないようにする必要がある！！！
class CreateFurniture(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str, Field(max_length=1000)]
    color: FurnitureColor
    # max_digits は Decimal の有効数字の総桁数(先行ゼロや末尾の無意味なゼロはカウントせず)
    # decimal_places は小数点以下の最大桁数を指定。つまり、全体で最大10桁、そのうち小数部は最大2桁。
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    featured: bool
    stock: Annotated[int, Field(ge=0)] # min=0は v1での書き方
    # EmailStrと違いHttpUrlは別途インストールする必要はない
    image_url: Annotated[HttpUrl|None, Field(max_length=256)] = None

    @field_serializer('image_url')
    def serialize_image_url(self, image_url: HttpUrl | None) -> str | None:
        if image_url is None: return None
        return str(image_url)



class UpdateFurniture(BaseModel):
    name: Annotated[str|None, Field(min_length=3, max_length=50)] = None
    description: Annotated[str|None, Field(max_length=1000)] = None
    color: FurnitureColor|None = None
    price: Annotated[Decimal|None, Field(gt=0, max_digits=10, decimal_places=2)] = None
    featured: bool|None = None
    stock: Annotated[int|None, Field(ge=0)] = None
    image_url: Annotated[HttpUrl|None, Field(max_length=256)] = None

    @field_serializer('image_url')
    def serialize_image_url(self, image_url: HttpUrl | None) -> str | None:
        if image_url is None: return None
        return str(image_url)


class ReadFurniture(BaseModel):
    id: Annotated[int, Field(ge=0)]
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str, Field(max_length=1000)]
    color: FurnitureColor
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    featured: bool
    stock: Annotated[int, Field(ge=0)] # min=0は v1での書き方
    # EmailStrと違いHttpUrlは別途インストールする必要はない
    image_url: Annotated[HttpUrl|None, Field(max_length=256)]
    created_at: datetime
    updated_at: datetime

    # model_configはPydantic V2で定められた、特別なクラス変数名
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('image_url')
    def serialize_image_url(self, image_url: HttpUrl | None) -> str | None:
        if image_url is None: return None
        return str(image_url)

class PublicFurniture(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str, Field(max_length=1000)]
    color: FurnitureColor
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    featured: bool
    stock: Annotated[int, Field(ge=0)] # min=0は v1での書き方
    # EmailStrと違いHttpUrlは別途インストールする必要はない
    image_url: Annotated[HttpUrl|None, Field(max_length=256)]

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('image_url')
    def serialize_image_url(self, image_url: HttpUrl | None) -> str | None:
        if image_url is None: return None
        return str(image_url)