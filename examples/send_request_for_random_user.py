import requests
import pandas as pd 
import json

if __name__ == "__main__":

    df = pd.read_csv('../data/dataset.csv', sep=";")

    param_dict = df.sample(1).to_dict(orient='records')[0]
    data = json.dumps(param_dict)

    print('Selected uuid:', param_dict['uuid'])

    # ec2 machine ip
    ip_address = '3.70.181.154' 

    headers = {} 
    headers["Content-Type"] = "application/json"


    response = requests.post(f'http://{ip_address}/predict-default-probability', headers=headers, data=data)
    print('API RESPONSE:', response.json())


