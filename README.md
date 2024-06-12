# Battle Pass Microservice

This project implements a simple battle pass system that can be accessed through a REST interface over HTTP. The system includes functionality for players to earn XP and level up in different battle passes.

## Project Structure

├── apigateway.tf
├── dynamodb.tf
├── iam.tf
├── initialize_battle_pass_data.py
├── lambda.tf
├── lambdas
│ ├── add_battle_pass_xp.py
│ ├── add_battle_pass_xp.zip
│ ├── get_battle_pass.py
│ └── get_battle_pass.zip
├── main.tf
├── outputs.tf
├── terraform.tfstate
├── terraform.tfstate.backup
├── variables.tf
└── tests
├── test_add_battle_pass_xp.py
└── test_get_battle_pass.py


## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/OlivaTac/aws-battlepass-microservice.git
    cd aws-battlepass-microservice
    ```

2. **Initialize Terraform:**

    ```bash
    terraform init
    ```

3. **Apply Terraform configuration:**

    ```bash
    terraform apply
    ```

    This will create all the necessary AWS resources, including DynamoDB tables, IAM roles, Lambda functions, and API Gateway.

4. **Populate initial Battle Pass data:**

    Run the `initialize_battle_pass_data.py` script to populate the `BattlePass_Data` table with initial data.

    ```bash
    python3 initialize_battle_pass_data.py
    ```

5. **Run Tests:**

    The tests are located in the `tests` directory. You can run them using `unittest`:

    ```bash
    python3 -m unittest discover tests
    ```

## API Endpoints

### Add Battle Pass XP

- **Endpoint:** `/add-battle-pass-xp`
- **Method:** `POST`
- **Headers:**
  - `player_id: string`
- **Body:**
    ```json
    {
      "battle_pass_id": "string",
      "earned_xp": integer
    }
    ```
- **Response:**
    - `200 OK` on success
      ```json
      {
        "battle_pass_id": "string",
        "title": "string",
        "level": integer,
        "xp": integer
      }
      ```
    - `400 Bad Request` if required parameters are missing
    - `404 Not Found` if the battle pass does not exist
    - `500 Internal Server Error` on server error

### Get Battle Pass Progress

- **Endpoint:** `/get-battle-pass-progress`
- **Method:** `POST`
- **Headers:**
  - `player_id: string`
- **Body:**
    ```json
    {
      "battle_pass_id": "string"
    }
    ```
- **Response:**
    - `200 OK` on success
      ```json
      {
        "battle_pass_id": "string",
        "title": "string",
        "level": integer,
        "xp": integer
      }
      ```
    - `400 Bad Request` if required parameters are missing
    - `404 Not Found` if the player progress does not exist
    - `500 Internal Server Error` on server error

## Notes

- Ensure you have the AWS CLI configured with appropriate permissions.
- The `initialize_battle_pass_data.py` script requires boto3 to be installed. You can install it using `pip`:

    ```bash
    pip install boto3
    ```

- Make sure to destroy the resources after testing to avoid unnecessary charges:

    ```bash
    terraform destroy
    ```

## License

This project is licensed under the MIT License.
