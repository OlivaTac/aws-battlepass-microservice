import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Reference the DynamoDB table
data_table = dynamodb.Table('BattlePass_Data')

# Data to be inserted
initial_data = [
    {"battle_pass_id": "season1", "level": 1, "title": "Adept"},
    {"battle_pass_id": "season1", "level": 2, "title": "Master"},
    {"battle_pass_id": "season2", "level": 1, "title": "Bronze"},
    {"battle_pass_id": "season2", "level": 2, "title": "Silver"},
    {"battle_pass_id": "season2", "level": 3, "title": "Gold"}
]

# Insert data
for item in initial_data:
    data_table.put_item(Item=item)

print("Initial data inserted successfully.")
