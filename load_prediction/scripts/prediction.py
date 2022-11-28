from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import pandas

from load_prediction import DATA_DIR
from load_prediction.utils.data_manipulators import Date
from load_prediction.utils.multi_processing import pmap


N_STATION = 28
N_EXP = 1000
N_WORKER = 8

PREDICTION_OUTPUT_DIR = DATA_DIR / "predictions"
LOAD_PREDICTION_FILE_NAME = "load_predict"

if __name__ == "__main__":
    hist_data = pandas.read_csv(DATA_DIR / "load_hist_data.csv")
    weather_data = pandas.read_csv(DATA_DIR / "weather_data.csv")
    prediction = pandas.read_csv(DATA_DIR / "probability_estimates.csv")

    for station_id in range(1, N_STATION + 1):
        temperature = weather_data.query(f"`Station ID` == {station_id}")["Temperature"].values
        hist_data.insert(len(hist_data.columns), f"Station_{station_id}_T", temperature, True)

    X_all_T = hist_data.drop(["Date", "Load"], axis=1)
    dates = list(map(Date, hist_data["Date"]))
    X_all_T.insert(1, "Days_of_Year", [d.days_in_year for d in dates], True)
    X_all_T.insert(2, "Year", [d.year for d in dates], True)
    X_all_T.insert(3, "Is_Holiday", [d.is_holiday for d in dates], True)
    features = ["Days_of_Year", "Year", "Is_Holiday", "Hour"]

    # Compute average temperature to be used as a feature as well as a training data
    Temp = pandas.DataFrame()
    temperatures = X_all_T.drop(features, axis=1)

    Y = hist_data["Load"]
    X_avg_T = X_all_T[features]
    X_avg_T.insert(len(X_avg_T.columns), "Temperature", temperatures.values.mean(axis=1), True)

    # Prepare input for prediction
    prediction_dates = list(map(Date, prediction["Date"]))
    prediction.insert(1, "Days_of_Year", [d.days_in_year for d in prediction_dates], True)
    prediction.insert(2, "Year", [d.year for d in prediction_dates], True)
    prediction.insert(3, "Is_Holiday", [d.is_holiday for d in prediction_dates], True)


    def process(n_random):
        # randomly split train and test data by 80% and 20%
        X_train, X_test, Y_train, Y_test = train_test_split(X_avg_T, Y, test_size=0.2, random_state=n_random)
        mdl_rf_load = RandomForestRegressor()
        mdl_rf_load.fit(X_train, Y_train)

        X_T = X_train[["Days_of_Year", "Year", "Hour"]]
        mdl_rf_T = RandomForestRegressor()
        mdl_rf_T.fit(X_T, X_train["Temperature"])

        X_pred = prediction.drop(["Date", "Daily Peak Probability"], axis=1)
        X_pred.insert(len(X_pred.columns), "Temperature", mdl_rf_T.predict(X_pred[["Days_of_Year", "Year", "Hour"]]),
                      True)

        # write out each prediction to a file
        answers = X_pred.copy()
        answers.insert(0, "Date", prediction["Date"], True)
        answers.insert(len(answers.columns), "Load", mdl_rf_load.predict(X_pred), True)
        answers = answers.drop(["Days_of_Year"], axis=1)
        answers.to_csv(PREDICTION_OUTPUT_DIR / f"{LOAD_PREDICTION_FILE_NAME}_{n_random}.csv")

    n_tries = [n for n in range(N_EXP)]
    pmap(process, n_tries, num_workers=N_WORKER)

    # plt.plot(X_1["Days_of_Year"], hist_data["Load"])
    # plt.show()
    # plt.scatter(hist_data["Hour"], hist_data["Load"])
    # plt.show()
    # plt.plot(X_pred["Days_of_Year"], answers["Load"])
    # plt.show()
    # plt.scatter(X_pred["Hour"], answers["Load"])
    # plt.show()