import json

import pandas as pd
import numpy as np
import uuid
from time import gmtime, strftime
from src.scorer import get_score
from src.api_facades import Product

class DbRecordMaker():

    def __init__(self, product_object: Product, keyword_searched: str):

        self.affiliate_tag = "ahorrarenca0b-21"
        self.keyword_searched = keyword_searched
        self.p = product_object
        self.timestamp = self.get_current_time()
        self.prod_id  = str(uuid.uuid4())


    @staticmethod
    def aec_score_schema():
        columns = ["product_id", "timestamp", "overall", "score_dist_amz", "fiability", "value", "pros", "cons"]
        dtypes = [str, str, float, np.array, float, float, str, str]
        return {k: v for k, v in zip(columns, dtypes)}

    @staticmethod
    def _reviews_schema():
        columns = ["review_id", "timestamp", "product_id", "asin", "title", "body", "link",
                   "rating", "post_date", "verified_purchase", "vine_program",
                   "country", "is_global_review", "has_images", "helpful_votes", "origin"]
        dtypes = [str, str, str, str, str, str, int, str, bool, bool, str, bool, bool, int, str]
        return {k: v for k, v in zip(columns, dtypes)}

    @staticmethod
    def product_schema():
        table_columns = ["product_id", "timestamp", "asin", "product_name", "title",
                         "keyword_searched", "keywords", "keywords_list", "parent_asin", "variant_asins",
                         "brand", "attributes", "price", "price_currency", "categories", "main_image_url",
                         "images_urls", "feature_bullets", "rating_avg", "ratings_count",
                         "five_star_count", "four_star_count", "three_star_count", "two_star_count", "one_star_count",
                         "similar_products"]
        #probs needs to be revisted
        dtypes = [str, str, str, str, str,
                  str, str, str, str, str,
                  str, str, float, str, str, str,
                  str, str, str, float, int,
                  int, int, int, int, int,
                  str]
        return {k: v for k, v in zip(table_columns, dtypes)}
    @staticmethod
    def get_current_time():
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def _get_product_record(self):

        prod_id = self.prod_id
        prod_name = self.p.title.split(",")[0]
        timestamp = self.timestamp
        price = float(self.p.price['value'])
        price_currency = self.p.price['currency']

        record = (prod_id, timestamp, self.p.asin, prod_name, self.p.title,
                  self.keyword_searched, self.p.keywords, self.p.keywords_list, self.p.parent_asin, self.p.variant_asins,
                  self.p.brand, self.p.attributes, price, price_currency, self.p.categories, self.p.main_image_url,
                  self.p.images_urls, self.p.feature_bullets, self.p.rating_avg, self.p.ratings_count,
                  self.p.five_star_count, self.p.four_star_count, self.p.three_star_count, self.p.two_star_count, self.p.one_star_count,
                  self.p.similar_products)

        return record

    def product_record(self):
        r = self._get_product_record()
        table_columns = list(self.product_schema().keys())
        rec = pd.DataFrame.from_records([r])
        rec.columns = table_columns
        return rec

    def reviews_records(self):
        """
        Returns review information as a pandas dataframe
        :return:
        """
        df_reviews = pd.DataFrame.from_records(self.p.top_reviews)

        if "date" in df_reviews.columns:
            df_reviews["date"] = df_reviews["date"].apply(lambda x: x.get("utc"))

        if "images" in df_reviews.columns:
            df_reviews["has_images"] = ~df_reviews["images"].isna()
        else:
            df_reviews["has_images"] = False

        df_reviews["timestamp"] = self.timestamp
        df_reviews["product_id"] = self.prod_id
        df_reviews["asin"] = self.p.asin
        df_reviews["origin"] = "amz"
        df_reviews = df_reviews.rename({"id": "review_id", "date": "post_date", "review_country": "country"}, axis=1)
        columns = self._reviews_schema().keys()

        # If columns do not exists, add them with None values
        for col in columns:
            if col not in df_reviews.columns:
                df_reviews[col] = None

        return df_reviews[columns]


    def _aec_score_record(self):
        rate_count = np.array([self.p.five_star_count, self.p.four_star_count,
                      self.p.three_star_count, self.p.two_star_count, self.p.one_star_count])
        outcomes = [5,4,3,2,1]
        score = get_score(rate_count, outcomes)
        overall = score["aec"]
        score_dist_amz = rate_count/rate_count.sum()
        fiability = None
        value = None
        pros = None
        cons = None
        return (self.prod_id, self.timestamp, overall, score_dist_amz, fiability, value, pros, cons)



    def aec_score_record(self):
        r = self._aec_score_record()
        schema = self.aec_score_schema()
        rec = pd.DataFrame.from_records([r])
        rec.columns = schema.keys()
        return rec
    def rating_distribution(self):
        """
        Returns the frequentist rating probability distribution as a numpy array
        :return:
        """
        d = self.rating_breakdown
        keys = ['five_star', 'four_star', 'three_star', 'two_star', 'one_star']
        return np.array([d[k]["count"] for k in keys]) / self.ratings_count

    def make_product_related_db_records(self):
        """
        This function takes the ASIN API request and the related search keyword and returns the records to be inserted in the database
        :param api_req:
        :param search_keyword:
        :return:
        """


        product_record = self.product_record()
        reviews_records = self.reviews_records()
        aec_score_record = self.aec_score_record()
        return product_record, reviews_records, aec_score_record


    # gets amazon afiliate linkg
    def amazon_afiliate_link(self, asin):
        return f"https://www.amazon.es/dp/{asin}/ref=nosim?tag={self.affiliate_tag}"

