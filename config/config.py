from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Composio MCP Configuration
COMPOSIO_API_KEY = os.getenv('COMPOSIO_API_KEY')
COMPOSIO_BASE_URL = os.getenv('COMPOSIO_BASE_URL', 'https://api.composio.dev')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Agent Configuration
AGENT_CONFIG = {
    'researcher': {
        'role': 'Researcher',
        'goal': 'Research and analyze data from Composio MCP',
        'backstory': 'An expert at analyzing MCP data and finding insights'
    },
    'analyst': {
        'role': 'Analyst',
        'goal': 'Process and interpret MCP data findings',
        'backstory': 'Specialized in interpreting MCP data and making recommendations'
    }
} 