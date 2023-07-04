import json
import pandas as pd

MAX_VARIANCE = 4

def get_expected_value(outcomes, p_measure):
    return (outcomes*p_measure).sum()

def get_variance(outcomes, p_measure):

    mu = get_expected_value(outcomes, p_measure)
    centered_outcomes = outcomes - mu
    variance = (centered_outcomes ** 2 * p_measure).sum()

    return variance

def to_score_df(score_breakdown):
    df = pd.DataFrame(score_breakdown).transpose()
    df["rating"] = [5, 4, 3, 2, 1]
    df = df.set_index("rating")
    return df

def get_score(x_count : pd.Series):

    p_measure = x_count/ x_count.sum()
    outcomes = df.index.values

    mean_score = get_expected_value(outcomes, p_measure)
    var_score = get_variance(outcomes, p_measure)

    aec_score = mean_score - var_score / MAX_VARIANCE

    return {"aec": aec_score, "mean_score": mean_score}

if __name__ == '__main__':

    with open('product_json.json') as f:
        data = json.load(f)

    score = data["product"]["rating_breakdown"]
    df = to_score_df(score)
    score=get_score(df["count"])