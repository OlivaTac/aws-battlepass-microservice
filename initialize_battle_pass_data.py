import boto3
import sys

def initialize_data(region):
    # Initialize the DynamoDB resource
    dynamodb = boto3.resource('dynamodb', region_name=region)

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

    print(f"Initial data inserted successfully in {region}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 initialize_battle_pass_data.py <region>")
        sys.exit(1)

    region = sys.argv[1]
    initialize_data(region)
