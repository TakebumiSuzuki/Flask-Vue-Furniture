from backend.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import datetime
from sqlalchemy import func


class Furniture(db.Model):
    __tablename__ = 'furnitures'

    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), index=True, unique=True)
    description: Mapped[str] = mapped_column(db.String(1000))
    color: Mapped[str] = mapped_column(db.String(20), index=True)
    # precision は有効数字の総桁数（小数点の前と後の数字の合計）を表し、
    # scale は小数点以下の桁数を表す。
    price: Mapped[Decimal] = mapped_column(db.Numeric(precision=10, scale=2), index=True)
    featured: Mapped[bool] = mapped_column(db.Boolean(), index=True)
    stock: Mapped[int] = mapped_column(db.Integer())
    image_url: Mapped[str|None] = mapped_column(db.String(256))
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f'<Furniture name:"{self.name}" color:{self.color} price:{self.price} image_url:{self.image_url}>'

