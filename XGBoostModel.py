from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from xgboost import XGBRegressor


class XGBoostModel:

    mean_squared_errors = []
    lowest_err_achieved = 999.9

    def __init__(self, objective, colsample_bytree, learning_rate, max_depth, alpha, n_estimators):
        self.objective = objective
        self.colsample_bytree = colsample_bytree
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.alpha = alpha
        self.n_estimators = n_estimators
        self.model = XGBRegressor(objective=objective,
                                  colsample_bytree=colsample_bytree,
                                  learning_rate=learning_rate,
                                  max_depth=max_depth,
                                  alpha=alpha,
                                  n_estimators=n_estimators)

    def train(self, x_train, y_train):
        self.model.fit(x_train, y_train)

    def predict_many(self, x_test):
        return self.model.predict(x_test)

    def predict_one(self, record):
        pass
        # TODO

    def evaluate_model(self, predictions, y_test):
        # err = mean_squared_error(y_test, predictions)
        # self.mean_squared_errors.append(err)
        # if err < self.lowest_err_achieved: self.lowest_err_achieved = err
        # return err
        return mean_absolute_percentage_error(y_test, predictions)