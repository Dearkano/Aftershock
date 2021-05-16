import numpy as np
import pandas as pd
import requests

if __name__ == "__main__":
    total_data = pd.read_csv('x.csv').to_numpy()
    total_labels = pd.read_csv('y.csv').to_numpy()
    test_X = total_data[0:5, :]
    test_y = total_labels[0:5, :]

    dict_case = {"data": [[0.01263237, 0.01085025, 0.99077399, 0.13449757, 0],
                          [0.01082759, 0.00790507, 0.99974728, 0.01804598, 0]]}

    # for AKS deployment you'd need to the service key in the header as well
    api_key = ''
    headers = {'Content-Type': 'application/json',  'Authorization': ('Bearer ' + api_key)}
    # headers = {'Content-Type': 'application/json'}

    url = "http://d65d760a-ffc8-471c-9d4a-61c05dc82b76.westus.azurecontainer.io/score"
    resp = requests.get(url, str(dict_case), headers=headers)
    print("POST to url", url)
    print("label:", test_y[0])
    print("prediction:", resp.text)
