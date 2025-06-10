import requests
import json
from config.settings import constants

def get_prediction(user_id):
    url = constants.SAGEMAKER_URL

    payload = json.dumps({
        "UserID": user_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["body"]