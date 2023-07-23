import json
import uuid
from time import gmtime, strftime

import numpy as np
import pandas as pd

from product_rater.api_facades import Product
from product_rater.scorer import get_score


class DbRecordMaker:
    def __init__(self, product_object: Product, aec_category: str):
        self.aec_category = aec_category
        self.p = product_object
        self.timestamp = self.get_current_time()
        self.prod_id = str(uuid.uuid4())

    @staticmethod
    def get_current_time():
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def _get_product_record(self):
        prod_id = self.prod_id
        prod_name = self.p.title.split(".")[0]
        timestamp = self.timestamp
        price = float(self.p.price["value"])
        price_currency = self.p.price["currency"]

        record = (
            prod_id,
            timestamp,
            self.p.asin,
            prod_name,
            self.p.title,
            self.aec_category,
            self.p.keywords,
            self.p.keywords_list,
            self.p.parent_asin,
            self.p.variant_asins,
            self.p.brand,
            self.p.attributes,
            price,
            price_currency,
            self.p.categories,
            self.p.main_image_url,
            self.p.images_urls,
            self.p.feature_bullets,
            self.p.rating_avg,
            self.p.ratings_count,
            self.p.five_star_count,
            self.p.four_star_count,
            self.p.three_star_count,
            self.p.two_star_count,
            self.p.one_star_count,
            self.p.similar_products,
        )

        return record

    def product_record(self):
        r = self._get_product_record()
        table_columns = [
            "product_id",
            "timestamp",
            "asin",
            "product_name",
            "title",
            "aec_category",
            "keywords",
            "keywords_list",
            "parent_asin",
            "variant_asins",
            "brand",
            "attributes",
            "price",
            "price_currency",
            "categories",
            "main_image_url",
            "images_urls",
            "feature_bullets",
            "rating_avg",
            "ratings_count",
            "five_star_count",
            "four_star_count",
            "three_star_count",
            "two_star_count",
            "one_star_count",
            "similar_products",
        ]
        rec = pd.DataFrame.from_records([r])
        rec.columns = table_columns
        return rec

    def reviews_records(self):
        """Returns review information as a pandas dataframe
        :return:
        """
        timestamp = self.timestamp
        df_reviews = pd.DataFrame.from_records(self.p.top_reviews)
        df_reviews["date"] = df_reviews["date"].apply(lambda x: x["utc"])
        df_reviews["timestamp"] = timestamp
        df_reviews["product_id"] = self.prod_id
        df_reviews["has_images"] = ~df_reviews["images"].isna()
        df_reviews["origin"] = "amz"
        df_reviews = df_reviews.rename(
            {"id": "review_id", "date": "post_date", "review_country": "country"},
            axis=1,
        )
        return df_reviews[
            [
                "review_id",
                "timestamp",
                "product_id",
                "title",
                "body",
                "link",
                "rating",
                "post_date",
                "verified_purchase",
                "vine_program",
                "country",
                "is_global_review",
                "has_images",
                "helpful_votes",
                "origin",
            ]
        ]

    def _aec_score_record(self):
        rate_count = np.array(
            [
                self.p.five_star_count,
                self.p.four_star_count,
                self.p.three_star_count,
                self.p.two_star_count,
                self.p.one_star_count,
            ]
        )
        outcomes = [5, 4, 3, 2, 1]
        overall, _ = get_score(rate_count, outcomes)
        score_dist_amz = rate_count / rate_count.sum()
        fiability = None
        value = None
        pros = None
        cons = None
        return (
            self.prod_id,
            self.timestamp,
            overall,
            score_dist_amz,
            fiability,
            value,
            pros,
            cons,
        )

    def aec_score_record(self):
        r = self._aec_score_record()
        columns = [
            "product_id",
            "timestamp",
            "overall",
            "score_dist_amz",
            "fiability",
            "value",
            "pros",
            "cons",
        ]
        rec = pd.DataFrame.from_records([r])
        rec.columns = columns
        return rec

    def rating_distribution(self):
        """Returns the frequentist rating probability distribution as a numpy array
        :return:
        """
        d = self.rating_breakdown
        keys = ["five_star", "four_star", "three_star", "two_star", "one_star"]
        return np.array([d[k]["count"] for k in keys]) / self.ratings_count


def make_product_related_db_records(api_req, search_keyword):
    """Takes the ASIN API request and the related search.

    keyword and returns the records to be inserted in the database.
    """
    p = Product(api_req)
    db_record_maker = DbRecordMaker(product_object=p, aec_category=search_keyword)
    product_record = db_record_maker.product_record()
    reviews_records = db_record_maker.reviews_records()
    aec_score_record = db_record_maker.aec_score_record()
    return product_record, reviews_records, aec_score_record


def populate_db_with_keyword_search(keyword):
    # get api response keyword search results
    # set up the request parameters

    # make the http GET request to Rainforest API
    # api_result = requests.get('https://api.rainforestapi.com/request', params)
    # api_req = api_result.json()

    # Load it for dev purposes
    with open(
        "data/keyword_search_json.json",
    ) as f:
        api_req = json.load(f)

    # filter best asin according to rating and number of reviews
    sr = pd.DataFrame.from_records(api_req["search_results"])
    best_asins = (
        sr[sr["ratings_total"] > 300]
        .sort_values("rating", ascending=False)
        .iloc[:10]
        .asin.values
    )

    # loop over best asins, get api request and make records
    for _asin in best_asins:
        # set up the request parameters

        # make the http GET request to Rainforest API
        # asin_req = requests.get('https://api.rainforestapi.com/request', params)

        with open(
            "notebooks/product_json.json",
        ) as f:
            asin_req = json.load(f)

        (
            product_record,
            reviews_records,
            aec_score_record,
        ) = make_product_related_db_records(asin_req, keyword)

        # insert records in db
        pass
