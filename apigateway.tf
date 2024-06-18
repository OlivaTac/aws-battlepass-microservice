// Define the API Gateway REST API
resource "aws_api_gateway_rest_api" "battlepass_api" {
  name        = "BattlePassAPI"
  description = "API for BattlePass Microservice"
  depends_on  = [aws_lambda_function.get_battle_pass_progress, aws_lambda_function.add_battle_pass_xp]
}

// Define the API Gateway resource for getting BattlePass progress
resource "aws_api_gateway_resource" "get_progress_resource" {
  rest_api_id = aws_api_gateway_rest_api.battlepass_api.id
  parent_id   = aws_api_gateway_rest_api.battlepass_api.root_resource_id
  path_part   = "get-battle-pass-progress"
}

// Define the API Gateway resource for adding BattlePass XP
resource "aws_api_gateway_resource" "add_xp_resource" {
  rest_api_id = aws_api_gateway_rest_api.battlepass_api.id
  parent_id   = aws_api_gateway_rest_api.battlepass_api.root_resource_id
  path_part   = "add-battle-pass-xp"
}

// Define the API Gateway method for getting BattlePass progress
resource "aws_api_gateway_method" "get_battle_pass_progress" {
  rest_api_id   = aws_api_gateway_rest_api.battlepass_api.id
  resource_id   = aws_api_gateway_resource.get_progress_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

// Integrate API Gateway with the Lambda function for getting BattlePass progress
resource "aws_api_gateway_integration" "lambda_integration_get" {
  rest_api_id             = aws_api_gateway_rest_api.battlepass_api.id
  resource_id             = aws_api_gateway_resource.get_progress_resource.id
  http_method             = aws_api_gateway_method.get_battle_pass_progress.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.get_battle_pass_progress.invoke_arn
}

// Define the API Gateway method for adding BattlePass XP
resource "aws_api_gateway_method" "add_battle_pass_xp" {
  rest_api_id   = aws_api_gateway_rest_api.battlepass_api.id
  resource_id   = aws_api_gateway_resource.add_xp_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

// Integrate API Gateway with the Lambda function for adding BattlePass XP
resource "aws_api_gateway_integration" "lambda_integration_add" {
  rest_api_id             = aws_api_gateway_rest_api.battlepass_api.id
  resource_id             = aws_api_gateway_resource.add_xp_resource.id
  http_method             = aws_api_gateway_method.add_battle_pass_xp.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.add_battle_pass_xp.invoke_arn
}

// Deploy the API Gateway
resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration_get,
    aws_api_gateway_integration.lambda_integration_add
  ]
  rest_api_id = aws_api_gateway_rest_api.battlepass_api.id
  stage_name  = "prod"
}
