import math
import os
import random

from joblib import dump, load
import numpy as np
import pandas as pd
from azureml.core import Workspace, Dataset
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor


def save_model(model_name, model):
    if not os.path.exists("./outputs"):
        os.makedirs("./outputs")
    file_name = f"{model_name}.pkl"
    dump(value=model, filename=f'./outputs/{file_name}')
    print(f"save the model: {model_name}")


def train_model(input_data, labels, train_percentage, model_name):
    # file_name = f"{model_name}_model.pkl"
    # if os.path.exists(f"./{file_name}"):
    #     print("model already exists")
    #     return load(f"./{file_name}")
    # split data
    N = input_data.shape[0]
    train_data_size = int(N * train_percentage)
    test_data_size = N - train_data_size
    print(f"train_data_size: " + str(train_data_size))
    print(f"test_data_size: " + str(test_data_size))
    train_X = input_data[0:train_data_size]
    train_y = labels[0:train_data_size]
    test_X = input_data[train_data_size:]
    test_y = labels[train_data_size:]

    # model = MLPRegressor(hidden_layer_sizes=2, learning_rate_init=0.01, activation="relu",
    #                      solver="adam", max_iter=500, verbose=True)
    # model = LinearRegression()
    model = RandomForestRegressor()
    model.fit(train_X, train_y)
    print("check the test performance set")
    test_output = model.predict(test_X)
    # calculate accuracy on the prediction
    rmse = np.sqrt(mean_squared_error(test_output, test_y))
    print('Root Mean Square deviation is', rmse)
    save_model(model_name, model)
    return model


def remove_outlier(input_data, input_labels):
    mean = np.mean(input_data, axis=0)
    standard_deviation = np.std(input_data, axis=0)
    # print(mean)
    # print(standard_deviation)
    data = []
    labels = []
    for i in range(input_data.shape[0]):
        check = True
        for j in range(input_data.shape[1]):
            if abs(input_data[i][j] - mean[j]) >= 2 * standard_deviation[j]:
                check = False
        if check:
            data.append(input_data[i])
            labels.append(input_labels[i])

    return np.asarray(data), np.asarray(labels)


def norm_data_range(input_data):
    for i in range(input_data.shape[1]):
        cur_min = np.min(input_data[:, i])
        cur_max = np.max(input_data[:, i])
        print(f"feature {i} min: {str(cur_min)}")
        print(f"feature {i} max: {str(cur_max)}")
        input_data[:, i] = input_data[:, i] - cur_min
        input_data[:, i] = input_data[:, i] / (cur_max - cur_min)
    return input_data


if __name__ == "__main__":
    # load the data
    features_path = "https://5412fpstorage.blob.core.windows.net/dataset/x.csv"
    labels_path = "https://5412fpstorage.blob.core.windows.net/dataset/y.csv"
    aftershock_features = Dataset.Tabular.from_delimited_files(path=features_path)
    aftershock_labels = Dataset.Tabular.from_delimited_files(path=labels_path)
    total_data = aftershock_features.to_pandas_dataframe().to_numpy()
    total_labels = aftershock_labels.to_pandas_dataframe().to_numpy()

    # total_data = pd.read_csv('x.csv').to_numpy()
    # total_labels = pd.read_csv('y.csv').to_numpy()
    # random_indices = random.sample(range(total_data.shape[0]), total_data.shape[0])
    # total_data = total_data[random_indices]
    # total_labels = total_labels[random_indices]
    # limit range of values of features to 0 to 1
    total_data, total_labels = remove_outlier(total_data, total_labels)
    total_data = norm_data_range(total_data)
    # # total_data = preprocessing.normalize(total_data)
    print(total_labels.shape)
    train_percentage = 0.8

    model = train_model(total_data, total_labels, train_percentage, "aftershock_model")
    print(model.predict(total_data[0:10, :]))


