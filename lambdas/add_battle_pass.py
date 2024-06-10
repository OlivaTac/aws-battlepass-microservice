import json
import boto3
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Reference the BattlePassProgress table
table = dynamodb.Table('BattlePassProgress')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        user_id = body['userId']
        season_id = body['seasonId']
        level = body['level']
        progress = body['progress']
        rewards_claimed = body['rewardsClaimed']
        
        table.put_item(
            Item={
                'userId': user_id,
                'seasonId': season_id,
                'level': level,
                'progress': progress,
                'rewardsClaimed': rewards_claimed
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'BattlePass progress added successfully'})
        }
    except Exception as e:
        logger.error(f"Error adding BattlePass progress: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }
