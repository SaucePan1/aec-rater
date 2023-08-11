import json
import numpy as np
import pytest

from src.api_facades import Product
from src.records import DbRecordMaker


class TestDbRecordMaker():

    @pytest.fixture
    def api_req(self):
        with open("data/product_json.json") as f:
            data = json.load(f)
        return data
    @pytest.fixture()
    def product_object(self, api_req):
        p = Product(api_req)
        return p

    def test_product_record(self, product_object):
        db_record_maker = DbRecordMaker(product_object=product_object, keyword_searched="robots cocina")
        db_record = db_record_maker.product_record()


        assert db_record["title"].iloc[0] == product_object.title
        assert db_record["asin"].iloc[0] == product_object.asin
        assert db_record["affiliate_link"].iloc[0] == 'https://www.amazon.es/dp/B0BGSRV33C/ref=nosim?tag=ahorrarenca0b-21'

    def test_reviews_records(self, product_object):
        db_record_maker = DbRecordMaker(product_object=product_object, keyword_searched="robots cocina")
        db_records = db_record_maker.reviews_records()

        assert db_records.shape == (8,15)
        assert db_records["asin"].iloc[0] == 'B0BGSRV33C'
        assert db_records["review_id"].iloc[0] == 'R34AJ865BZXBNA'
        assert len(db_records["body"].iloc[0]) == 1928

    def test_aec_score_record(self, product_object):
        db_record_maker = DbRecordMaker(product_object=product_object, keyword_searched="robots cocina")
        db_record = db_record_maker.aec_score_record()

        assert db_record.shape == (1, 8)
        assert np.isclose(db_record["overall"].iloc[0], 3.8262)

    def test_make_product_related_db_records(self, product_object):
        db_record_maker = DbRecordMaker(product_object=product_object, keyword_searched="robots cocina")
        product_record, reviews_records, aec_score_record = db_record_maker.make_product_related_db_records()

        assert product_record.shape == (1, 26)
        assert reviews_records.shape == (8, 15)
        assert aec_score_record.shape == (1, 8)

        assert product_record["asin"].iloc[0] == 'B0BGSRV33C'
        assert reviews_records["asin"].iloc[0] == 'B0BGSRV33C'
        assert aec_score_record["asin"].iloc[0] == 'B0BGSRV33C'

        assert reviews_records["rating"].iloc[0] == 4