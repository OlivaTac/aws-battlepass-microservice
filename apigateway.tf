// Define the API Gateway REST API
resource "aws_api_gateway_rest_api" "battlepass_api" {
  name        = "BattlePassAPI"
  description = "API for BattlePass Microservice"
}

// Define the API Gateway resource
resource "aws_api_gateway_resource" "battlepass" {
  rest_api_id = aws_api_gateway_rest_api.battlepass_api.id
  parent_id   = aws_api_gateway_rest_api.battlepass_api.root_resource_id
  path_part   = "battlepass"
}

// Define the API Gateway method for getting BattlePass progress
resource "aws_api_gateway_method" "get_battle_pass" {
  rest_api_id   = aws_api_gateway_rest_api.battlepass_api.id
  resource_id   = aws_api_gateway_resource.battlepass.id
  http_method   = "GET"
  authorization = "NONE"
}

// Integrate API Gateway with the Lambda function for getting BattlePass progress
resource "aws_api_gateway_integration" "lambda_integration_get" {
  rest_api_id             = aws_api_gateway_rest_api.battlepass_api.id
  resource_id             = aws_api_gateway_resource.battlepass.id
  http_method             = aws_api_gateway_method.get_battle_pass.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.get_battle_pass_progress.invoke_arn
}

// Define the API Gateway method for adding BattlePass progress
resource "aws_api_gateway_method" "post_battle_pass" {
  rest_api_id   = aws_api_gateway_rest_api.battlepass_api.id
  resource_id   = aws_api_gateway_resource.battlepass.id
  http_method   = "POST"
  authorization = "NONE"
}

// Integrate API Gateway with the Lambda function for adding BattlePass progress
resource "aws_api_gateway_integration" "lambda_integration_add" {
  rest_api_id             = aws_api_gateway_rest_api.battlepass_api.id
  resource_id             = aws_api_gateway_resource.battlepass.id
  http_method             = aws_api_gateway_method.post_battle_pass.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.add_battle_pass_progress.invoke_arn
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
