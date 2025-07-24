from uuid import UUID
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[
        str,
        Field(
            min_length=7,
            pattern=r"^(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$", # 少なくとも1つの数字、1つの特殊文字を含む
        )
    ]


class UpdateUsernameUser(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]


class UpdatePasswordUser(BaseModel):
    raw_password: Annotated[
        str,
        Field(
            min_length=7,
            pattern=r"^(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$", # 少なくとも1つの数字、1つの特殊文字を含む
        )
    ]


class ReadUser(BaseModel):
    id: UUID
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    is_admin: bool
    token_valid_after: datetime|None
    created_at: datetime
    last_login_at: datetime|None


class PublicUser(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr