// Define the DynamoDB table for storing BattlePass progress
resource "aws_dynamodb_table" "battlepass" {
  name         = "BattlePassProgress"
  billing_mode = "PAY_PER_REQUEST" // Billing mode, free tier eligible
  hash_key     = "userId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "seasonId"
    type = "S" // String
  }

  global_secondary_index {
    name            = "SeasonIndex"
    hash_key        = "seasonId"
    projection_type = "ALL"
  }
}
