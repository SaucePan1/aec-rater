import json

from product_rater.scorer import get_score, to_score_df

if __name__ == "__main__":
    with open("notebooks/product_json.json") as f:
        data = json.load(f)

    score = data["product"]["rating_breakdown"]
    df = to_score_df(score)
    score = get_score(df["count"], [])
