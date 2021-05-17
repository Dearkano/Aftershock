import numpy as np
import azureml.core
from azureml.core import Workspace, Experiment, Run
from azureml.core import ScriptRunConfig
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
import os
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import Model
from azureml.core.webservice import AciWebservice
import uuid
from azureml.core.webservice import Webservice
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core import Workspace
from azureml.core.model import Model

model_names = ["day_mag1_2_sk_model", "day_mag3_4_sk_model", "day_mag_above_5_sk_model", "week_mag1_2_sk_model",
               "week_mag3_4_sk_model", "week_mag_above_5_sk_model", "month_mag1_2_sk_model",
               "month_mag3_4_sk_model", "month_mag_above_5_sk_model"]


def create_compute_resource(ws):
    # choose a name for your cluster
    compute_name = os.environ.get("AML_COMPUTE_AFTERSHOCK_CLUSTER", "cpu-cluster")
    compute_min_nodes = os.environ.get("AML_COMPUTE_AFTERSHOCK_CLUSTER_MIN_NODES", 0)
    compute_max_nodes = os.environ.get("AML_COMPUTE_AFTERSHOCK_CLUSTER_MAX_NODES", 4)

    # This example uses CPU VM. For using GPU VM, set SKU to STANDARD_NC6
    vm_size = os.environ.get("AML_COMPUTE_AFTERSHOCK_CLUSTER_SKU", "STANDARD_D2_V2")

    if compute_name in ws.compute_targets:
        compute_target = ws.compute_targets[compute_name]
        if compute_target and type(compute_target) is AmlCompute:
            print("found compute target: " + compute_name)
    else:
        print("creating new compute target...")
        provisioning_config = AmlCompute.provisioning_configuration(vm_size=vm_size,
                                                                    min_nodes=compute_min_nodes,
                                                                    max_nodes=compute_max_nodes)

        # create the cluster
        compute_target = ComputeTarget.create(ws, compute_name, provisioning_config)

        # can poll for a minimum number of nodes and for a specific timeout.
        # if no min node count is provided it will use the scale settings for the cluster
        compute_target.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)

        # For a more detailed view of current AmlCompute status, use get_status()
        print(compute_target.get_status().serialize())
    return compute_target


def Azure_ML_experiment():

    # create experiment
    experiment_name = 'aftershock-model-train'
    exp = Experiment(workspace=ws, name=experiment_name)

    # creation of compute task
    compute_target = create_compute_resource(ws)

    # to install required packages
    env = Environment('aftershock-env-01')
    cd = CondaDependencies.create(pip_packages=['azureml-dataset-runtime[pandas,fuse]',
                                                'azureml-defaults'],
                                  conda_packages=['scikit-learn==0.24.2'])

    env.python.conda_dependencies = cd

    src = ScriptRunConfig(source_directory=os.getcwd(),
                          script='train.py',
                          arguments=[],
                          compute_target=compute_target,
                          environment=env)

    # submit the train script to the experiment
    run = exp.submit(config=src)
    print(run.get_file_names())


def register_model():
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


def deploy_models():
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
    env = Environment.get(workspace=ws, name='aftershock-env')

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


if __name__ == "__main__":
    # check core SDK version number
    print("Azure ML SDK Version: ", azureml.core.VERSION)

    # connect to workspace
    subscription_id = '937625ed-b6d9-4759-be33-95b1637d200b'
    resource_group = 'FinalProject'
    workspace_name = 'Aftershock_Prediction_Model'

    ws = Workspace(subscription_id, resource_group, workspace_name)
    print(ws.name, ws.location, ws.resource_group, sep='\t')

    # run ML experiment in Azure service
    # Azure_ML_experiment()

    # register and deploy the model
    # output_model = register_model()
    deploy_models()

