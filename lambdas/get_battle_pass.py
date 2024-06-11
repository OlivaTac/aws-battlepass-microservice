import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Reference the DynamoDB tables
progress_table = dynamodb.Table('BattlePass_Progress')
data_table = dynamodb.Table('BattlePass_Data')

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
    try:
        # Validate headers
        if 'headers' not in event or 'player_id' not in event['headers']:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required header: player_id'})
            }

        player_id = event['headers']['player_id'].strip()

        # Validate body
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing request body'})
            }

        body = json.loads(event['body'])

        if 'battle_pass_id' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required parameter: battle_pass_id'})
            }

        battle_pass_id = body['battle_pass_id']

        # Fetch player progress
        response = progress_table.get_item(
            Key={
                'player_id': player_id,
                'battle_pass_id': battle_pass_id
            }
        )

        if 'Item' in response:
            # If player progress exists, retrieve current level and XP
            player_progress = response['Item']
            level = int(player_progress['level'])
            xp = int(player_progress['xp'])

            # Fetch title from battle pass data
            data_response = data_table.get_item(
                Key={
                    'battle_pass_id': battle_pass_id,
                    'level': level
                }
            )

            if 'Item' in data_response:
                title = data_response['Item']['title']

                # Return the player's current progress in the battle pass
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'battle_pass_id': battle_pass_id,
                        'title': title,
                        'level': level,
                        'xp': xp
                    }, default=decimal_to_float)
                }
            else:
                # If the battle pass level is not found, return an error
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Battle pass level not found'})
                }
        else:
            # If the player progress is not found, return an error
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Player progress not found'})
            }
    except Exception as e:
        # Handle any exceptions that occur
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
