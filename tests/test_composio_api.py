import unittest
from unittest.mock import patch, MagicMock
from src.composio_api import ComposioAPI

class TestComposioAPI(unittest.TestCase):
    def setUp(self):
        self.api = ComposioAPI()

    @patch('requests.request')
    def test_make_request_success(self, mock_request):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response

        # Test the request
        result = self.api.make_request('test-endpoint')
        
        # Verify the result
        self.assertEqual(result, {'data': 'test'})
        mock_request.assert_called_once()

    @patch('requests.request')
    def test_make_request_error(self, mock_request):
        # Setup mock to raise an exception
        mock_request.side_effect = Exception('Test error')

        # Test the request raises an exception
        with self.assertRaises(Exception):
            self.api.make_request('test-endpoint')

if __name__ == '__main__':
    unittest.main() 