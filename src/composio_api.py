import requests
from config.config import COMPOSIO_API_KEY, COMPOSIO_BASE_URL

class ComposioAPI:
    def __init__(self):
        self.api_key = COMPOSIO_API_KEY
        self.base_url = COMPOSIO_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def make_request(self, endpoint, method='GET', data=None):
        """
        Make a request to the Composio MCP API
        
        Args:
            endpoint (str): API endpoint
            method (str): HTTP method (GET, POST, etc.)
            data (dict): Request payload
            
        Returns:
            dict: API response
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request to Composio MCP: {str(e)}")

    def get_mcp_data(self):
        """
        Get data from Composio MCP
        
        Returns:
            dict: MCP data
        """
        return self.make_request('data')  # Replace 'data' with actual endpoint

    def send_mcp_command(self, command_data):
        """
        Send a command to Composio MCP
        
        Args:
            command_data (dict): Command payload
            
        Returns:
            dict: Command response
        """
        return self.make_request('command', method='POST', data=command_data)  # Replace 'command' with actual endpoint 