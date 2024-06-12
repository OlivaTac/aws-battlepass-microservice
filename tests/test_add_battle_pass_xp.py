import unittest
from unittest.mock import patch, MagicMock
import json
from lambdas.add_battle_pass_xp import lambda_handler

class TestAddBattlePassXP(unittest.TestCase):

    @patch('lambdas.add_battle_pass_xp.progress_table.get_item')
    @patch('lambdas.add_battle_pass_xp.progress_table.put_item')
    @patch('lambdas.add_battle_pass_xp.data_table.query')
    @patch('lambdas.add_battle_pass_xp.data_table.get_item')
    def test_add_xp_new_player(self, mock_get_item, mock_query, mock_put_item, mock_get_progress):
        # Mock the DynamoDB responses for a new player
        mock_get_progress.return_value = {}
        mock_query.return_value = {'Items': [{'level': 1}, {'level': 2}], 'Count': 2}
        mock_get_item.return_value = {'Item': {'title': 'Adept'}}
        
        # Create a mock event for the Lambda function
        event = {
            'headers': {'player_id': 'player1'},
            'body': json.dumps({'battle_pass_id': 'season1', 'earned_xp': 50})
        }
        
        # Call the Lambda function with the mock event
        response = lambda_handler(event, None)
        
        # Print response for debugging
        print("Response for test_add_xp_new_player:", response)
        
        # Check that the response is as expected
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['level'], 0)
        self.assertEqual(body['xp'], 50)
        self.assertEqual(body['title'], "")

    @patch('lambdas.add_battle_pass_xp.progress_table.get_item')
    @patch('lambdas.add_battle_pass_xp.progress_table.put_item')
    @patch('lambdas.add_battle_pass_xp.data_table.query')
    @patch('lambdas.add_battle_pass_xp.data_table.get_item')
    def test_add_xp_existing_player(self, mock_get_item, mock_query, mock_put_item, mock_get_progress):
        # Mock the DynamoDB responses for an existing player
        mock_get_progress.return_value = {'Item': {'player_id': 'player1', 'battle_pass_id': 'season1', 'level': 0, 'xp': 50}}
        mock_query.return_value = {'Items': [{'level': 1}, {'level': 2}], 'Count': 2}
        mock_get_item.return_value = {'Item': {'title': 'Adept'}}
        
        # Create a mock event for the Lambda function
        event = {
            'headers': {'player_id': 'player1'},
            'body': json.dumps({'battle_pass_id': 'season1', 'earned_xp': 50})
        }
        
        # Call the Lambda function with the mock event
        response = lambda_handler(event, None)
        
        # Print response for debugging
        print("Response for test_add_xp_existing_player:", response)
        
        # Check that the response is as expected
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['level'], 1)
        self.assertEqual(body['xp'], 0)
        self.assertEqual(body['title'], "Adept")

    @patch('lambdas.add_battle_pass_xp.data_table.query')
    def test_add_xp_invalid_battle_pass(self, mock_query):
        # Mock the DynamoDB response for an invalid battle pass
        mock_query.return_value = {'Items': [], 'Count': 0}

        # Create a mock event for the Lambda function
        event = {
            'headers': {'player_id': 'player1'},
            'body': json.dumps({'battle_pass_id': 'invalid_season', 'earned_xp': 50})
        }

        # Call the Lambda function with the mock event
        response = lambda_handler(event, None)

        # Print response for debugging
        print("Response for test_add_xp_invalid_battle_pass:", response)

        # Check that the response is as expected
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('Battle pass not found', response['body'])

if __name__ == '__main__':
    unittest.main()
