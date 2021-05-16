import json
import joblib
import numpy as np
import pandas as pd
import requests
from sklearn import preprocessing


def norm_data_range(input_data):
    for i in range(5):
        cur_min = np.min(input_data[:, i])
        cur_max = np.max(input_data[:, i])
        print(f"feature {i} min: {str(cur_min)}")
        print(f"feature {i} max: {str(cur_max)}")
        input_data[:, i] = input_data[:, i] - cur_min
        input_data[:, i] = input_data[:, i] / (cur_max - cur_min)
    return input_data


if __name__ == "__main__":
    total_data = pd.read_csv('x.csv').to_numpy()
    data_x = [[0.0975609756097562, 0.4125451071959244, 0.025346534653465348,
               0.17139478200672079, 0.0008739348918505571]]
    dict_case = {"data": data_x, "model_name": "day_mag1_2"}
    json_case = json.dumps(dict_case)
    data = np.array(json.loads(json_case)['data'])
    model_name = json.loads(json_case)['model_name']
    print(data)
    print(model_name)

    # load the model
    model = joblib.load("./aftershock_model.pkl")
    # test api request data
    print(model.predict(data))
    # Test all data
    res = model.predict(norm_data_range(total_data))
    # check positive predicted results
    print(res.shape[0] * res.shape[1])
    print(np.sum(res >= 0))
    # the result is a Python dictionary:

