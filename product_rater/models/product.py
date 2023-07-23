"""Product model."""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base


class Product(Base):
    """Product model."""

    id: Mapped[str] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    asin: Mapped[str]
    name: Mapped[str]
    title: Mapped[str]
    category: Mapped[str]
    keywords: Mapped[str]
    keywords_list: Mapped[str]
    parent_asin: Mapped[str]
    variant_asins: Mapped[str]
    brand: Mapped[str]
    price: Mapped[float]
    price_currency: Mapped[str]
    categories: Mapped[str]
    main_image_url: Mapped[str]
    images_urls: Mapped[str]
    feature_bullets: Mapped[str]
    rating_avg: Mapped[float]
    ratings_count: Mapped[int]
    five_star_count: Mapped[int]
    four_star_count: Mapped[int]
    three_star_count: Mapped[int]
    two_star_count: Mapped[int]
    one_star_count: Mapped[int]
    similar_products: Mapped[str]
