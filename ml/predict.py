import json
import numpy as np
import joblib
from azureml.core.model import Model
from azureml.core import Workspace

subscription_id = 'a53d5b1a-ed1b-4bd9-bc58-ea489ce7da2d'
resource_group = 'CS5412'
workspace_name = 'Aftershock_Forecast'
ws = Workspace(subscription_id, resource_group, workspace_name)
print(ws.name, ws.location, ws.resource_group, sep='\t')


def init():
    global model
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # For multiple models, it points to the folder containing all deployed models (./azureml-models)
    model_path = Model.get_model_path("aftershock_model", _workspace=ws)
    model = joblib.load(model_path)


def run(raw_data):
    print("arrive the API")
    print("raw data")
    print(raw_data)
    print(type(raw_data))
    data = np.array(json.loads(raw_data)['data'])
    print("data")
    print(data)
    # make prediction
    y_hat = model.predict(data)
    # you can return any data type as long as it is JSON-serializable
    return y_hat.tolist()
