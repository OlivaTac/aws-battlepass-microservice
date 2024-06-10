import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Reference the BattlePassProgress table
table = dynamodb.Table('BattlePassProgress')

# Helper function to convert DynamoDB item to JSON serializable format
def decimal_to_float(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = decimal_to_float(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj:
            obj[k] = decimal_to_float(obj[k])
        return obj
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Log the received event

    try:
        # Extract userId and seasonId from the query string parameters
        user_id = event['queryStringParameters']['userId']
        season_id = event['queryStringParameters']['seasonId']
        
        # Query the table using the Global Secondary Index (GSI) for the given seasonId
        response = table.query(
            IndexName='SeasonIndex',
            KeyConditionExpression=Key('seasonId').eq(season_id)
        )
        
        # Filter the items by userId
        items = [item for item in response['Items'] if item['userId'] == user_id]
        
        # Check if the filtered query returned any items
        if items:
            # If items were found, return the first item with a 200 status code
            item = decimal_to_float(items[0])
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            # If no items were found, return a 404 status code with an error message
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
    except Exception as e:
        print("Error:", str(e))  # Log any errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
