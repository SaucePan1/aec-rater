"""First revision

Revision ID: d40a68b6bf27
Revises:
Create Date: 2023-07-22 17:34:27.224549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d40a68b6bf27"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("asin", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("keywords", sa.String(), nullable=False),
        sa.Column("keywords_list", sa.String(), nullable=False),
        sa.Column("parent_asin", sa.String(), nullable=False),
        sa.Column("variant_asins", sa.String(), nullable=False),
        sa.Column("brand", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("price_currency", sa.String(), nullable=False),
        sa.Column("categories", sa.String(), nullable=False),
        sa.Column("main_image_url", sa.String(), nullable=False),
        sa.Column("images_urls", sa.String(), nullable=False),
        sa.Column("feature_bullets", sa.String(), nullable=False),
        sa.Column("rating_avg", sa.Float(), nullable=False),
        sa.Column("ratings_count", sa.Integer(), nullable=False),
        sa.Column("five_star_count", sa.Integer(), nullable=False),
        sa.Column("four_star_count", sa.Integer(), nullable=False),
        sa.Column("three_star_count", sa.Integer(), nullable=False),
        sa.Column("two_star_count", sa.Integer(), nullable=False),
        sa.Column("one_star_count", sa.Integer(), nullable=False),
        sa.Column("similar_products", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", "timestamp"),
    )
    op.create_table(
        "review",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("product_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("body", sa.String(), nullable=False),
        sa.Column("link", sa.String(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("post_date", sa.DateTime(), nullable=False),
        sa.Column("verified_purchase", sa.Boolean(), nullable=False),
        sa.Column("vine_program", sa.Boolean(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("is_global_review", sa.Boolean(), nullable=False),
        sa.Column("has_images", sa.Boolean(), nullable=False),
        sa.Column("helpful_votes", sa.Integer(), nullable=False),
        sa.Column("origin", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id", "timestamp"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("review")
    op.drop_table("product")
    # ### end Alembic commands ###
