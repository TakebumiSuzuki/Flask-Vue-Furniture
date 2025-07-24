from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from backend.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(db.Uuid(), primary_key=True, default=lambda: uuid4())
    username: Mapped[str] = mapped_column(db.String(50), unique=True)
    email: Mapped[str] = mapped_column(db.String(256), unique=True)
    password: Mapped[str] = mapped_column(db.String(256))
    is_admin: Mapped[bool] = mapped_column(db.Boolean(), default=False)
    token_valid_after: Mapped[datetime|None] = mapped_column(db.DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )
    last_login_at: Mapped[datetime|None] = mapped_column(db.DateTime(timezone=True))

    def __repr__(self):
        return f'<User id:{self.id} username:"{self.username}" email:{self.email} is_admin:{self.is_admin} token_valid_after:{self.token_valid_after} created_at:{self.created_at} last_login_at:{self.last_login_at} >'



