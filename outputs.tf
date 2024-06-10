// Output the REST API URL
output "rest_api_url" {
  value = "${aws_api_gateway_deployment.deployment.invoke_url}/prod/battlepass"
}
