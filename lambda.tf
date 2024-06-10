// Define the Lambda function for getting BattlePass progress
resource "aws_lambda_function" "get_battle_pass_progress" {
  function_name = "GetBattlePassProgress"
  handler       = "get_battle_pass.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "lambdas/get_battle_pass.zip" // Adjusted path

  source_code_hash = filebase64sha256("lambdas/get_battle_pass.zip") // Adjusted path
}

// Define the Lambda function for adding BattlePass progress
resource "aws_lambda_function" "add_battle_pass_progress" {
  function_name = "AddBattlePassProgress"
  handler       = "add_battle_pass.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "lambdas/add_battle_pass.zip" // Adjusted path

  source_code_hash = filebase64sha256("lambdas/add_battle_pass.zip") // Adjusted path
}

// Add permission for API Gateway to invoke the get BattlePass Lambda function
resource "aws_lambda_permission" "allow_apigw_invoke_get" {
  statement_id  = "AllowAPIGatewayInvokeGet"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_battle_pass_progress.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.aws_account_id}:${aws_api_gateway_rest_api.battlepass_api.id}/*/*/battlepass"
}

// Add permission for API Gateway to invoke the add BattlePass Lambda function
resource "aws_lambda_permission" "allow_apigw_invoke_add" {
  statement_id  = "AllowAPIGatewayInvokeAdd"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.add_battle_pass_progress.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.aws_account_id}:${aws_api_gateway_rest_api.battlepass_api.id}/*/*/battlepass"
}
