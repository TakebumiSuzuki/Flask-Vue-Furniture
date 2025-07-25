from backend.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func


class BlockedToken(db.Model):
    __tablename__ = 'blocked_tokens'

    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    jti: Mapped[str] = mapped_column(db.String(36), index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self):
        return f'<BlockedToken id:{self.id} created_at:{self.created_at} jti:{self.jti} >'