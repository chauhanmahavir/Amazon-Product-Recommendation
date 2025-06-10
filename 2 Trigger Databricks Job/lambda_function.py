import json
import requests
import os

def lambda_handler(event, context):
    # TODO implement
    file_name = event["Records"][0]["s3"]["object"]["key"]
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    print("Bucket: " + bucket_name)
    print("Key: " + file_name)

    # Databricks API Details
    databricks_token = os.environ['DATABRICKS_API_TOKEN']  # Replace with your Databricks API Token
    databricks_url = f'{os.environ["DATABRICKS_URL"]}#/api/2.0/jobs/run-now'  # Databricks API URL (replace <databricks-instance> with your Databricks workspace URL)
    
    headers = {
        'Authorization': f'Bearer {databricks_token}',
        'Content-Type': 'application/json',
    }

    # Create JSON payload with necessary job details (replace job_id with your Databricks job ID)
    payload = {
        "job_id": os.environ['JOB_ID'],
        "notebook_params": {
            "file_name": file_name,
            "bucket_name": bucket_name
        }
    }

    # Send API request to Databricks
    response = requests.post(databricks_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print(f"Successfully triggered Databricks job for file {file_name} in bucket {bucket_name}")
    else:
        print(f"Failed to trigger Databricks job. Status Code: {response.status_code}, Response: {response.text}")
    return {
        'statusCode': 200,
        'body': json.dumps('Triggered Databricks job successfully')
    }