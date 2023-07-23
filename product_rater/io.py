import pandas as pd

class IO:
    """
    Class to read and write data

    Parameters:
    ----------
    path_to_data: str
        Path to the data folder
    reviews: str
        Name of the reviews file
    products: str
        Name of the products file
    aec_scores: str
        Name of the aec_scores file
    """
    def __init__(self):
        self.path_to_data= "data/"
        self.reviews = "reviews.csv"
        self.products = "products.csv"
        self.aec_scores = "aec_scores.csv"

    def read_reviews(self):
        return pd.read_csv(self.path_to_data + self.reviews)

    def read_products(self):
        return pd.read_csv(self.path_to_data + self.products)

    def read_aec_scores(self):
        return pd.read_csv(self.path_to_data + self.aec_scores)

    def append_reviews(self, reviews):
        reviews.to_csv(self.path_to_data + self.reviews, mode="a", header=False, index=False)

    def append_products(self, products):
        products.to_csv(self.path_to_data + self.products, mode="a", header=False, index=False)

    def append_aec_scores(self, aec_scores):
        aec_scores.to_csv(self.path_to_data + self.aec_scores, mode="a", header=False, index=False)

    def write_reviews(self, reviews):
        reviews.to_csv(self.path_to_data + self.reviews, index=False)

    def write_products(self, products):
        products.to_csv(self.path_to_data + self.products, index=False)

    def write_aec_scores(self, aec_scores):
        aec_scores.to_csv(self.path_to_data + self.aec_scores, index=False)



