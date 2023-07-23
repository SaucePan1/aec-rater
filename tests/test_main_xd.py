import pytest
import pandas as pd

from main import remove_asins_found_in_products_csv

def test_remove_asins_found_in_products_csv():

    best_asins = ["B07XJ8C8F5", "B0BGSRV33C"]
    new_best_asins = remove_asins_found_in_products_csv(best_asins, "../data/products.csv")
    assert len(new_best_asins) == 1