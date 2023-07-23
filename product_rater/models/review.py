"""Review model."""

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base


class Review(Base):
    """Product model."""

    id: Mapped[str] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("product.id"))
    title: Mapped[str]
    body: Mapped[str]
    link: Mapped[str]
    rating: Mapped[int]
    post_date: Mapped[datetime]
    verified_purchase: Mapped[bool]
    vine_program: Mapped[bool]
    country: Mapped[str]
    is_global_review: Mapped[bool]
    has_images: Mapped[bool]
    helpful_votes: Mapped[int]
    origin: Mapped[str]
