from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Composio MCP Configuration
COMPOSIO_API_KEY = os.getenv('COMPOSIO_API_KEY')
COMPOSIO_BASE_URL = os.getenv('COMPOSIO_BASE_URL', 'https://api.composio.dev')  # Replace with actual base URL

class ComposioAPI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def make_request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data
        )
        return response.json()

# Initialize Composio API client
composio = ComposioAPI(COMPOSIO_API_KEY, COMPOSIO_BASE_URL)

# Create CREW AI Agents
researcher = Agent(
    role='Researcher',
    goal='Research and analyze data from Composio MCP',
    backstory='An expert at analyzing MCP data and finding insights',
    verbose=True
)

analyst = Agent(
    role='Analyst',
    goal='Process and interpret MCP data findings',
    backstory='Specialized in interpreting MCP data and making recommendations',
    verbose=True
)

# Define Tasks
research_task = Task(
    description='Gather and analyze data from Composio MCP',
    agent=researcher
)

analysis_task = Task(
    description='Interpret the gathered data and provide recommendations',
    agent=analyst
)

# Create and run the crew
crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    verbose=2,
    process=Process.sequential
)

# Execute the crew's tasks
result = crew.kickoff()

print("Crew AI Analysis Results:")
print(result) 