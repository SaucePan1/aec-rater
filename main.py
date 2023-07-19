import json
from src.scorer import to_score_df, get_score

if __name__ == '__main__':

    with open('notebooks/product_json.json') as f:
        data = json.load(f)

    score = data["product"]["rating_breakdown"]
    df = to_score_df(score)
    score=get_score(df["count"])