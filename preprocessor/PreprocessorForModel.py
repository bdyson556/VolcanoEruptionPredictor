# goals: engineer features and return x_train, x_test, y_train, y_test
from numpy import genfromtxt
from sklearn.model_selection import train_test_split


class PreprocessorForModel:

    def load_csv_to_NumPy(self, csv_path, headers=False):

        # Load raw CSV data. Ignore header.
        skip_header = 1 if headers else 0
        dataset = genfromtxt(csv_path, delimiter=",", skip_header=skip_header)
        shape = dataset.shape
        # Split data into X and y (features and labels). Ignore id column.
        xs = dataset[:, 1:-1]
        ys = dataset[:, -1]
        return xs, ys, shape

    def split_data(self, xs, ys):
        # split data into train and test sets
        seed = 7
        test_size = 0.33
        return train_test_split(xs, ys, test_size=test_size, random_state=seed)

    def engineer_features(self):
        pass
        # TODO


if __name__ == "__main__":
    preprocessor = PreprocessorForModel()
    preprocessor.load_csv_to_NumPy("preprocessor/prepared_observations.csv", True)
