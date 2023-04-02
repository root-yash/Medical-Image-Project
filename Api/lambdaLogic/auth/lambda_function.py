import json
import boto3 

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    
    response = client.get_item(
        TableName = "Auth-Table",
        Key = {
            'KeyID': {
                "S": event["KeyID"]
            }
        }
    )
    data = response.get("Item", {})
    if data:
        return {
            "AuthComplete": data["Key"]["S"] ==  event["Key"]
        }
    else:
        return {
            "AuthComplete": False
        }
        