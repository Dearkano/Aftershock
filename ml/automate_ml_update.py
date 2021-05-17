from joblib import dump
import os
import numpy as np
from azureml.core import Workspace, Dataset
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import azureml.core
import os
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core import Workspace
from azureml.core.model import Model


def save_model(model_name, model):
    if not os.path.exists("./outputs"):
        os.makedirs("./outputs")
    file_name = f"{model_name}.pkl"
    dump(value=model, filename=f'./outputs/{file_name}')
    print(f"save the model: {model_name}")


def train_model(input_data, labels, train_percentage, model_name):
    N = input_data.shape[0]
    train_data_size = int(N * train_percentage)
    test_data_size = N - train_data_size
    print(f"train_data_size: " + str(train_data_size))
    print(f"test_data_size: " + str(test_data_size))
    train_X = input_data[0:train_data_size]
    train_y = labels[0:train_data_size]
    test_X = input_data[train_data_size:]
    test_y = labels[train_data_size:]

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


def train_aftershock_model():
    print("train aftershock prediction model")
    # load the data
    features_path = "https://5412fpstorage.blob.core.windows.net/dataset/x.csv"
    labels_path = "https://5412fpstorage.blob.core.windows.net/dataset/y.csv"
    aftershock_features = Dataset.Tabular.from_delimited_files(path=features_path)
    aftershock_labels = Dataset.Tabular.from_delimited_files(path=labels_path)
    total_data = aftershock_features.to_pandas_dataframe().to_numpy()
    total_labels = aftershock_labels.to_pandas_dataframe().to_numpy()

    total_data, total_labels = remove_outlier(total_data, total_labels)
    total_data = norm_data_range(total_data)
    train_percentage = 0.8
    train_model(total_data, total_labels, train_percentage, "aftershock_model")


def register_model(ws):
    model_path = "./outputs/aftershock_model.pkl"
    model_name = "aftershock_model"
    print(model_path)
    model = Model.register(model_path=model_path,
                           model_name=model_name,
                           tags={"data": "earthquakes", "model": "aftershock_predictor"},
                           description="predict aftershocks based on earthquake features",
                           workspace=ws)
    print(model.name, model.id, model.version, sep='\t')
    return model


def deploy_models(ws):
    aciconfig = AciWebservice.deploy_configuration(cpu_cores=1,
                                                   memory_gb=1,
                                                   tags={"data": "Earthquake", "method": "sklearn"},
                                                   description='Predict aftershock situation '
                                                               'using linear models in sklearn')
    # env = Environment('aftershock-env')
    # cd = CondaDependencies.create(pip_packages=['azureml-dataset-runtime[pandas,fuse]',
    #                                             'azureml-defaults'],
    #                               conda_packages=['scikit-learn==0.24.2'])
    # env.python.conda_dependencies = cd
    env = Environment.get(workspace=ws, name="aftershock-env")

    inference_config = InferenceConfig(entry_script="predict.py", environment=env)
    model = Model(ws, "aftershock_model")

    # service_name = 'sklearn-aftershock-svc-' + str(uuid.uuid4())[:4]
    service_name = "sklearn-aftershock-svc-f41b"
    service = Model.deploy(workspace=ws,
                           name=service_name,
                           models=[model],
                           overwrite=True,
                           inference_config=inference_config,
                           deployment_config=aciconfig)

    service.wait_for_deployment(show_output=True)
    print(service.get_logs())
    print(service.scoring_uri)
    print("service keys")
    print(service.get_keys())
    print("service token")
    print(service.get_token())


def update_Azure_ML_Service():
    # check core SDK version number
    print("Azure ML SDK Version: ", azureml.core.VERSION)

    # connect to workspace
    subscription_id = '937625ed-b6d9-4759-be33-95b1637d200b'
    resource_group = 'FinalProject'
    workspace_name = 'Aftershock_Prediction_Model'

    ws = Workspace(subscription_id, resource_group, workspace_name)
    print(ws.name, ws.location, ws.resource_group, sep='\t')

    # register and deploy the model
    print("register and deploy the model")
    # register_model(ws)
    # deploy_models(ws)


if __name__ == "__main__":
    train_aftershock_model()
    update_Azure_ML_Service()
