import pandas
import numpy as np

from load_prediction import DATA_DIR
from load_prediction.scripts.prediction import N_EXP
from load_prediction.utils.data_manipulators import PredictionDF

PREDICTIONS_DIR = DATA_DIR / "predictions"
PROB_INPUT = PREDICTIONS_DIR.parent / "probability_estimates.csv"
PROB_OUTPUT = PREDICTIONS_DIR.parent / "output/probability_estimates.csv"
OUTPUT_VOTE = False


if __name__ == "__main__":
    prediction_df = pandas.read_csv(PROB_INPUT)
    prediction_df["Vote"] = np.zeros(len(prediction_df), dtype=int)

    all_dates = set(prediction_df["Date"].values)

    for file in PREDICTIONS_DIR.iterdir():
        predict_df = PredictionDF(file)
        date_to_peak = {date: predict_df.peak_hour_on_date(date) for date in all_dates}
        for date, hour in date_to_peak.items():
            row_idx = prediction_df.query(f"Date == '{date}' & Hour == {hour}")["Vote"].index
            prediction_df.loc[row_idx, "Vote"] += 1
    if OUTPUT_VOTE:
        prediction_df.to_csv(PREDICTIONS_DIR.parent / "output/vote_out.csv")

    prediction_df["Daily Peak Probability"] = prediction_df["Vote"] / N_EXP
    prediction_df = prediction_df.drop(["Vote"], axis=1)
    prediction_df.to_csv(PROB_OUTPUT)
