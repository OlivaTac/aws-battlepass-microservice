import unittest
from unittest.mock import patch, MagicMock
import json
from lambdas.get_battle_pass import lambda_handler

class TestGetBattlePass(unittest.TestCase):

    @patch('lambdas.get_battle_pass.progress_table.get_item')
    @patch('lambdas.get_battle_pass.data_table.get_item')
    def test_get_progress_existing_player(self, mock_get_item, mock_get_progress):
        # Mock the DynamoDB responses for an existing player
        mock_get_progress.return_value = {'Item': {'player_id': 'player1', 'battle_pass_id': 'season1', 'level': 1, 'xp': 50}}
        mock_get_item.return_value = {'Item': {'title': 'Adept'}}
        
        # Create a mock event for the Lambda function
        event = {
            'headers': {'player_id': 'player1'},
            'body': json.dumps({'battle_pass_id': 'season1'})
        }
        
        # Call the Lambda function with the mock event
        response = lambda_handler(event, None)
        
        # Print response for debugging
        print("Response for test_get_progress_existing_player:", response)
        
        # Check that the response is as expected
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['level'], 1)
        self.assertEqual(body['xp'], 50)
        self.assertEqual(body['title'], "Adept")

    @patch('lambdas.get_battle_pass.progress_table.get_item')
    def test_get_progress_nonexistent_player(self, mock_get_progress):
        # Mock the DynamoDB response for a non-existent player
        mock_get_progress.return_value = {}
        
        # Create a mock event for the Lambda function
        event = {
            'headers': {'player_id': 'player2'},
            'body': json.dumps({'battle_pass_id': 'season1'})
        }
        
        # Call the Lambda function with the mock event
        response = lambda_handler(event, None)
        
        # Print response for debugging
        print("Response for test_get_progress_nonexistent_player:", response)
        
        # Check that the response is as expected
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('Player progress not found', response['body'])

if __name__ == '__main__':
    unittest.main()
