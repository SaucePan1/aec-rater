import json

import pytest

from product_rater.api_facades import Product
from product_rater.records import DbRecordMaker


class TestDbRecordMaker:
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
        db_record_maker = DbRecordMaker(
            product_object=product_object, aec_category="robots cocina"
        )
        db_record = db_record_maker.product_record()

        assert db_record["title"].iloc[0] == product_object.title

    def test_reviews_records(self, product_object):
        db_record_maker = DbRecordMaker(
            product_object=product_object, aec_category="robots cocina"
        )
        db_records = db_record_maker.reviews_records()

        assert db_records.shape == (8, 15)

    def test_aec_score_record(self, product_object):
        db_record_maker = DbRecordMaker(
            product_object=product_object, aec_category="robots cocina"
        )
        db_record = db_record_maker.aec_score_record()

        assert db_record.shape == (1, 8)
