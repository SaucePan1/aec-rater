

class Product():

    """
    This class is a facade for the product API response. It is used to extract the information needed for the application.
    """
    def __init__(self, api_req):

        p = api_req["product"]
        self.title = p["title"]
        self.keywords = p["keywords"]
        self.asin = p["asin"]
        self.keywords_list = p["keywords_list"]
        self.parent_asin = p["parent_asin"]
        self.brand = p["brand"]
        self.variant_asins = p["variant_asins_flat"]
        self.main_image_url = p["main_image"]["link"]
        self.images_urls = p["images_flat"]
        self.feature_bullets = p["feature_bullets"]
        self.attributes = p["attributes"]
        self.price = p["buybox_winner"]["price"]  # Price is not clear which one is it, double check
        self.categories = p["categories_flat"]

        self.rating_avg = p["rating"]
        self.rating_breakdown = p["rating_breakdown"]
        keys = ['five_star', 'four_star', 'three_star', 'two_star', 'one_star']
        self.five_star_count, self.four_star_count, self.three_star_count, self.two_star_count, self.one_star_count \
            = [self.rating_breakdown[k]["count"] for k in keys]
        self.ratings_count = p["ratings_total"]
        self.top_reviews = p["top_reviews"]

        self.similar_products = api_req["compare_with_similar"]

