// Define the DynamoDB table for BattlePass Data
resource "aws_dynamodb_table" "battlepass_data" {
  name         = "BattlePass_Data"
  billing_mode = "PAY_PER_REQUEST" //free tier eligible
  hash_key     = "battle_pass_id"
  range_key    = "level"

  attribute {
    name = "battle_pass_id"
    type = "S"
  }

  attribute {
    name = "level"
    type = "N"
  }
}

// Define the DynamoDB table for BattlePass Progress
resource "aws_dynamodb_table" "battlepass_progress" {
  name         = "BattlePass_Progress"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "player_id"
  range_key    = "battle_pass_id"

  attribute {
    name = "player_id"
    type = "S"
  }

  attribute {
    name = "battle_pass_id"
    type = "S"
  }

  global_secondary_index {
    name            = "PlayerBattlePassIndex"
    hash_key        = "player_id"
    range_key       = "battle_pass_id"
    projection_type = "ALL"
  }
}
