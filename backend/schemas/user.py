import re
from uuid import UUID
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


# --- パスワード検証ロジックを共通化するための関数 ---
def validate_password(password: str) -> str:
    """パスワードが要件を満たしているか検証する"""
    if not re.search(r'\d', password):
        raise ValueError('パスワードには少なくとも1つの数字を含める必要があります。')
    if not re.search(r'[@$!%*?&]', password):
        raise ValueError('パスワードには少なくとも1つの特殊文字 (@$!%*?&) を含める必要があります。')
    return password


class CreateUser(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    # patternを削除し、Fieldでは文字数のみをチェック
    password: Annotated[str, Field(min_length=7)]

    model_config = ConfigDict(from_attributes=True)

    # passwordフィールドに対するカスタムバリデータを追加
    @field_validator('password', mode='after')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        return validate_password(v)


class ChangeUsernameUser(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]

    model_config = ConfigDict(from_attributes=True)

class ChangePasswordUser(BaseModel):
    old_password: str
    # new_passwordも同様にpatternを削除
    new_password: Annotated[str, Field(min_length=7)]

    # new_passwordフィールドに対するカスタムバリデータを追加
    @field_validator('new_password', mode='after')
    @classmethod
    def validate_new_password_strength(cls, v: str) -> str:
        return validate_password(v)

    model_config = ConfigDict(from_attributes=True)


class ReadUser(BaseModel):

    id: UUID
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    is_admin: bool
    token_valid_after: datetime|None
    created_at: datetime
    last_login_at: datetime|None

    model_config = ConfigDict(from_attributes=True)


class PublicUser(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)