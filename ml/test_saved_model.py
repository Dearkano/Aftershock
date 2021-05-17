import json
import joblib
import numpy as np
import pandas as pd
import requests
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error

mins = [5.0, 385, -0.423, 0]
maxs = [6.1, 572, 254.1, 331]


def norm_data_range(input_data):
    for i in range(4):
        input_data[:, i] = input_data[:, i] - mins[i]
        input_data[:, i] = input_data[:, i] / (maxs[i] - mins[i])
    return input_data


if __name__ == "__main__":
    total_data = pd.read_csv('x.csv').to_numpy()[:1000, :]
    test_y = pd.read_csv('y.csv').to_numpy()[:1000, :]
    data_x = np.asarray([[6.6, 677, 10, 1]])
    data_x = norm_data_range(data_x)
    # dict_case = {"data": data_x, "model_name": "day_mag1_2"}
    # json_case = json.dumps(dict_case)
    # data = np.array(json.loads(json_case)['data'])
    # model_name = json.loads(json_case)['model_name']
    # print(data)
    # print(model_name)

    # load the model
    model = joblib.load("./outputs/aftershock_model.pkl")
    # test api request data
    print(model.predict(data_x))

    # Test all data
    res = model.predict(norm_data_range(total_data))
    print(np.sqrt(mean_squared_error(res, test_y)))
    # check positive predicted results
    # print(res.shape[0] * res.shape[1])
    # print(np.sum(res >= 0))
    # the result is a Python dictionary:

