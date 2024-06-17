# Battle Pass Microservice

This project implements a simple battle pass system that can be accessed through a REST interface over HTTP. The system includes functionality for players to earn XP and level up in different battle passes.

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

3. **Zip the Lambda functions:**

    ```bash
    cd lambdas
    zip add_battle_pass_xp.zip add_battle_pass_xp.py
    zip get_battle_pass.zip get_battle_pass.py
    cd ..
    ```

4. **Create and Select Terraform Workspaces:**

    ```bash
    terraform workspace new ca-central-1
    terraform workspace new us-east-2
    ```

5. **Apply Terraform configuration for each region:**

    For `ca-central-1`:

    ```bash
    terraform workspace select ca-central-1
    terraform apply -var="aws_region=ca-central-1"
    ```

    For `us-east-2`:

    ```bash
    terraform workspace select us-east-2
    terraform apply -var="aws_region=us-east-2"
    ```

6. **Populate initial Battle Pass data:**

    Run the `initialize_battle_pass_data.py` script to populate the `BattlePass_Data` table with initial data.

    ```bash
    python3 initialize_battle_pass_data.py
    ```

7. **Run Tests:**

    The tests are located in the `tests` directory. You can run them using `unittest`:

    ```bash
    python3 -m unittest discover tests
    ```

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

## Running Tests

To ensure your implementation handles expected usage and error cases, you can run unit tests provided in the `tests` directory.

### Example Test Cases:

1. **Add XP for a new player:**

    - **Description:** Adds XP for a player who does not have existing progress in the specified battle pass.
    - **Expected Result:** The player's progress is created with the specified XP and level.

2. **Add XP for an existing player:**

    - **Description:** Adds XP for a player who already has progress in the specified battle pass.
    - **Expected Result:** The player's XP is updated correctly, and the level is adjusted if the XP threshold is crossed.

3. **Add XP with an invalid battle pass ID:**

    - **Description:** Tries to add XP using an invalid battle pass ID.
    - **Expected Result:** A `404 Not Found` response indicating the battle pass does not exist.

4. **Get progress for an existing player:**

    - **Description:** Retrieves the progress of a player in a specified battle pass.
    - **Expected Result:** The correct progress details, including XP, level, and title, are returned.

5. **Get progress for a nonexistent player:**

    - **Description:** Tries to get progress for a player who has no progress in the specified battle pass.
    - **Expected Result:** A `404 Not Found` response indicating the player progress does not exist.

## License

This project is licensed under the MIT License.

## Project Structure

```plaintext
.
├── apigateway.tf
├── dynamodb.tf
├── iam.tf
├── initialize_battle_pass_data.py
├── lambda.tf
├── lambdas
│   ├── add_battle_pass_xp.py
│   ├── add_battle_pass_xp.zip
│   ├── get_battle_pass.py
│   └── get_battle_pass.zip
├── main.tf
├── outputs.tf
├── terraform.tfstate
├── terraform.tfstate.backup
├── variables.tf
└── tests
    ├── test_add_battle_pass_xp.py
    └── test_get_battle_pass.py
