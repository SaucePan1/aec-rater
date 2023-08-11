import json
import pandas as pd
import requests

from typing import List

from src.records import DbRecordMaker
from src.api_facades import Product
from src.io import IO
from src.request_params import API_KEY, AMZ_DOMAIN

class DFContextManager:
    """
    This is probably useless but I wanted to try Context Managers.
    """
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.df = None

    def __enter__(self):
        self.df = pd.read_csv(self.csv_file_path)
        return self.df

    def __exit__(self, exc_type, exc_value, traceback):
        self.df = None

def remove_asins_found_in_products_csv(best_asins: List[str], csv_file_path: str) -> List[str]:

    with DFContextManager(csv_file_path) as df:
        asins = df.asin.values
        best_asins = set(best_asins)
        new_best_asins = best_asins - set(asins)
        print("Removing asins already in db: ", best_asins - new_best_asins)
        best_asins = list(new_best_asins)

    return best_asins

def populate_db_with_keyword_search(keyword: str, n_products: int = 10, min_ratings: int = 300,  dev_mode=False, save_results=True):

    if dev_mode == False:
        save_results = True

    # get api response keyword search results
    # set up the request parameters
    params = {
        'api_key': API_KEY,
        'amazon_domain': AMZ_DOMAIN,
        'type': 'search',
        'search_term': keyword
    }

    # make the http GET request to Rainforest API

    if dev_mode == True:
        SEARCH_JSON_FILE = "filtros_de_aire_req.json"
    # Load it for dev purposes
        with open(SEARCH_JSON_FILE,) as f:
            api_req = json.load(f)
    else:
        print("Making search request")
        api_result = requests.get('https://api.rainforestapi.com/request', params)
        api_req = api_result.json()

    try:
        #filter best asin according to rating and number of reviews
        print(f"Request successful: {len(api_req['search_results'])} products found")
        print(f"Credits remaining: {api_req['request_info']['credits_remaining']}")
        sr = pd.DataFrame.from_records(api_req["search_results"])
        best_asins = sr[sr["ratings_total"] > min_ratings].sort_values("rating", ascending=False).iloc[:n_products].asin.values

        if dev_mode == False:
            best_asins = remove_asins_found_in_products_csv(best_asins, "data/products.csv")


        print("Search request successful")
        print("Asins to look up: ", best_asins)



        # loop over best asins, get api request and make records
        for asin in best_asins:
            print("Making asin request for asin: ", asin)
            try:
                # set up the request parameters
                params = {
                    'api_key': API_KEY,
                    'amazon_domain': AMZ_DOMAIN,
                    'type': 'product',
                    'asin': asin
                }

                if dev_mode == True:
                    try:
                        asin_json_file = str(asin) + "_asin_req.json"
                        with open(asin_json_file,) as f:
                            asin_req = json.load(f)
                    except:
                        print("No asin json file found, for asin: ", asin)
                        pass
                else:
                    # make the http GET request to Rainforest API
                    asin_req = requests.get('https://api.rainforestapi.com/request', params).json()

                product_request = Product(asin_req)
                print(product_request.title)
                rmaker = DbRecordMaker(product_request, keyword)
                product_record, reviews_records, aec_score_record = rmaker.make_product_related_db_records()

                # save results
                print("Data extraction successful, saving results ", save_results)
                if save_results == True:
                    io = IO()
                    io.append_reviews(reviews_records)
                    io.append_products(product_record)
                    io.append_aec_scores(aec_score_record)

            except Exception as e:
                print(e)
                if dev_mode == False:
                    with open(str(asin) + "_asin_req.json", "w") as fp:
                        json.dump(asin_req, fp)

    except Exception as e:
        print(e)
        if dev_mode == False:
            with open("_".join(str(keyword).split(" "))+'_req.json', 'w') as fp:
                json.dump(api_req, fp)


if __name__ == '__main__':

    populate_db_with_keyword_search("auriculares bluetooth", n_products=15, dev_mode= False, save_results= False)



