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

        if 'earned_xp' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required parameter: earned_xp'})
            }

        battle_pass_id = body['battle_pass_id']
        earned_xp = int(body['earned_xp'])

        # Fetch player progress
        response = progress_table.get_item(
            Key={
                'player_id': player_id,
                'battle_pass_id': battle_pass_id
            }
        )

        if 'Item' in response:
            # If player progress exists, retrieve current XP and level
            player_progress = response['Item']
            current_xp = int(player_progress['xp'])
            current_level = int(player_progress['level'])
        else:
            # If player progress does not exist, initialize with 0 XP and level
            current_xp = 0
            current_level = 0

        # Calculate new XP and level
        new_xp = current_xp + earned_xp
        new_level = current_level

        # Fetch all levels for the given battle pass
        data_response = data_table.query(
            KeyConditionExpression=Key('battle_pass_id').eq(battle_pass_id)
        )
        max_level = len(data_response['Items'])

        # Level up the player while they have enough XP and haven't reached max level
        while new_xp >= 100 and new_level < max_level:
            new_xp -= 100
            new_level += 1

        title = "Max Level"
        # Determine the title for the current level
        if new_level < max_level or (new_level == 0 and new_xp < 100):
            title_response = data_table.get_item(
                Key={
                    'battle_pass_id': battle_pass_id,
                    'level': new_level + 1 if new_level == 0 else new_level
                }
            )
            if 'Item' in title_response:
                title = title_response['Item']['title']
        elif new_level == max_level:
            title_response = data_table.get_item(
                Key={
                    'battle_pass_id': battle_pass_id,
                    'level': max_level
                }
            )
            if 'Item' in title_response:
                title = title_response['Item']['title']

        # Update or create the player progress in the database
        progress_table.put_item(
            Item={
                'player_id': player_id,
                'battle_pass_id': battle_pass_id,
                'level': Decimal(new_level),
                'xp': Decimal(new_xp)
            }
        )

        # Return the updated player progress
        return {
            'statusCode': 200,
            'body': json.dumps({
                'battle_pass_id': battle_pass_id,
                'title': title,
                'level': new_level,
                'xp': new_xp
            }, default=decimal_to_float)
        }
    except Exception as e:
        # Handle any exceptions that occur
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
