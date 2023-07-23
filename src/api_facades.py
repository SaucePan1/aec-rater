import numpy as np


class Product():

    """
    This class is a facade for the product API response. It is used to extract the information needed for the application.
    """
    def __init__(self, api_req):

        p = api_req.get("product", {})
        self.title = p.get("title", "Title not found")
        self.keywords = p.get("keywords", "Keywords not found")
        self.asin = p.get("asin", "ASIN not found")
        self.keywords_list = p.get("keywords_list", ["Keywords list not found"])
        self.parent_asin = p.get("parent_asin", "Parent ASIN not found")
        self.brand = p.get("brand", "Brand not found")
        self.variant_asins = p.get("variant_asins_flat", ["Variant ASINS not found"])
        self.main_image_url = p.get("main_image", {}).get("link", "Main image not found")
        self.images_urls = p.get("images_flat", "Images not found")
        self.feature_bullets = p.get("feature_bullets", ["Feature bullets not found"])
        self.attributes = p.get("attributes", [])
        self.price = p.get("buybox_winner", {}).get("price", np.NAN)  # Price is not clear which one is it, double check
        self.categories = p.get("categories_flat", "Categories not found")

        self.rating_avg = p.get("rating", np.NAN)
        self.rating_breakdown = p.get("rating_breakdown", {})
        keys = ['five_star', 'four_star', 'three_star', 'two_star', 'one_star']
        self.five_star_count, self.four_star_count, self.three_star_count, self.two_star_count, self.one_star_count \
            = [self.rating_breakdown.get(k, {}).get("count") for k in keys]
        self.ratings_count = p.get("ratings_total", np.NAN)
        self.top_reviews = p.get("top_reviews", [])
        self.similar_products = api_req.get("compare_with_similar", [])


