import logging
import os
import sys

import Logger
from XGBoostModel import XGBoostModel
from configuration import CSV_PATH
from preprocessor.PreprocessorForCSV import PreprocessorForCSV
from preprocessor.PreprocessorForModel import PreprocessorForModel
from configuration import *
import matplotlib.pyplot as plt
import seaborn as sns


LOGGER = Logger.get_logger()
feature_names = ["volcano_id", "observ_id", "G", "rho", "mu", "rc", "M", "sigma", "time_remaining", "sensor_reading"]




def main():
    # Prepare CSV file of raw input data
    # CSV_preprocessor = PreprocessorForCSV()
    # CSV_preprocessor.prepare_data_object()

    # Load from CSV and split into train and test data.
    model_preprocessor = PreprocessorForModel()

    xs, ys, shape = model_preprocessor.load_csv_to_NumPy(CSV_PATH, True)
    LOGGER.info(f"Loaded raw dataset as array of {shape[1]} COLUMNS and {shape[0]} ROWS.")
    for i in range(shape[1]):
        sns.histplot(xs[:, i], bins=20, kde=True)
        plt.title(f'Histogram of {feature_names[i]}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.show()


    # Visualize
    # fig, axes = plt.subplots(nrows=shape[1], ncols=1, figsize=(8, 6 * shape[1]))
    # for i in range (0, shape[1]):
    #     sns.histplot(xs[:, i], ax=axes[i], kde=True)  # You can also use plt.hist() if you prefer
    #     axes[i].set_title(f'Histogram of {feature_names[i]}')
    #     axes[i].set_xlabel(feature_names[i])
    #     axes[i].set_ylabel('Frequency')
    # plt.tight_layout()
    # plt.show()

    # for i in range(xs.shape[1]):
    #     plt.hist(xs[:, i], bins=20, alpha=0.5, label=feature_names[i])
    # plt.xlabel('Value')
    # plt.ylabel('Frequency')
    # plt.title('Histograms of Features')
    # plt.legend()
    # plt.show()

    x_train, x_test, y_train, y_test = model_preprocessor.split_data(xs, ys)
    LOGGER.info(
        f"Split x and y values using last element as y value. Ignoring id column at idx 0.")  # X values:\n\t{xs[:3]} ...\nY values:\n\t{ys[:3]} ...")

    # Build model
    LOGGER.info("Building the model...")
    model = XGBoostModel(objective, colsample_bytree, learning_rate, max_depth, alpha, n_estimators)
    model.train(x_train, y_train)

    # Make predictions
    predictions = model.predict_many(x_test)
    LOGGER.info("Generated predictions.")
    # mean_squared_error = model.evaluate_model(predictions, y_test)
    # LOGGER.info(f"===== MEAN SQUARED ERROR: {mean_squared_error} =====")
    mean_abs_percent_error = model.evaluate_model(predictions, y_test)
    LOGGER.info(f"===== MEAN ABSOLUTE PERCENTAGE ERROR: {mean_abs_percent_error} =====")
    # print(predictions)
    # print(y_test)

if __name__ == "__main__":
    main()

