import json
import os
import boto3
import csv
import numpy as np

ENDPOINT_NAME = os.environ["ENDPOINT_NAME"]
runtime = boto3.client("runtime.sagemaker")

def lambda_handler(event, context):
    print("Recived event: " + json.dumps(event))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, 
                                       ContentType="text/csv", 
                                       Body=payload)
    
    print(response)
    
    result = response["Body"].read().decode()
    print(result)
    floatArr = np.fromstring(result, dtype=float, sep=', ')
    print(floatArr.shape)
    predictedLabel = np.argmax(floatArr)
    print("Predicted Class Label: {}.".format(predictedLabel))

    return {
        'statusCode': 200,
        'body': [int(predictedLabel)]
    }
