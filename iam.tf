//Lambda execution role
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role_${terraform.workspace}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

//Attaching the Lambda Policy 
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

//Policy to allow for actions on DynamoDB
resource "aws_iam_role_policy" "dynamodb_policy" {
  name = "dynamodb_policy_${terraform.workspace}"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Effect = "Allow"
        Resource = [
          aws_dynamodb_table.battlepass_data.arn,
          aws_dynamodb_table.battlepass_progress.arn,
          "${aws_dynamodb_table.battlepass_data.arn}/index/*",
          "${aws_dynamodb_table.battlepass_progress.arn}/index/*"
        ]
      }
    ]
  })
}
