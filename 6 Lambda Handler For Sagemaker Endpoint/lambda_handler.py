import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    sagemaker_runtime = boto3.client('runtime.sagemaker')

    endpoint_name = "<endpoint-name>"

    print("User ID:",event["UserID"])

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(event)
    )

    result = response['Body'].read().decode()

    print(result)

    return {
        'statusCode': 200,
        'body': json.loads(result)
    }

