from crewai import Agent, Task, Crew, Process
from config.config import AGENT_CONFIG, GROQ_API_KEY, GROQ_MODEL
from src.composio_api import ComposioAPI
from utils.helpers import format_mcp_data, save_results
from utils.search_api import google_search
from utils.scraper import run_scraper
import logging
import groq

logger = logging.getLogger(__name__)

class CrewAgents:
    def __init__(self):
        self.composio = ComposioAPI()
        self.groq_client = groq.Client(api_key=GROQ_API_KEY)
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self):
        """Create CREW AI agents with Groq LLM"""
        agents = {}
        
        # Create Web Scraper agent
        agents['scraper'] = Agent(
            role="Web Intelligence Gatherer",
            goal="Gather comprehensive information about steel industry, market trends, and company activities",
            backstory="Expert at collecting and analyzing steel industry data with deep knowledge of JSW Steel and competitors",
            verbose=True,
            llm=self._create_groq_llm(),
            tools=[google_search, run_scraper]
        )
        
        # Create Researcher agent
        agents['researcher'] = Agent(
            role="Steel Industry Analyst",
            goal="Analyze steel production data, market trends, and competitive landscape",
            backstory="Experienced steel industry analyst with expertise in production metrics and market dynamics",
            verbose=True,
            llm=self._create_groq_llm()
        )
        
        # Create Analyst agent
        agents['analyst'] = Agent(
            role="Strategic Insights Generator",
            goal="Generate actionable insights and strategic recommendations for steel industry operations",
            backstory="Strategic advisor with deep understanding of steel manufacturing and market positioning",
            verbose=True,
            llm=self._create_groq_llm()
        )
        
        return agents

    def _create_groq_llm(self):
        """Create Groq LLM configuration"""
        return {
            "model": GROQ_MODEL,
            "api_key": GROQ_API_KEY,
            "temperature": 0.7,
            "max_tokens": 4096
        }

    def _create_tasks(self):
        """Create tasks for the agents"""
        tasks = []
        
        # Web scraping and search task
        tasks.append(Task(
            description=(
                'Search for and analyze recent developments in the steel industry, focusing on: \n'
                '1. JSW Steel production capacity and utilization\n'
                '2. Raw material pricing and availability\n'
                '3. Market demand and steel pricing trends\n'
                '4. Competitor activities and market share\n'
                '5. Environmental regulations and compliance'
            ),
            agent=self.agents['scraper']
        ))
        
        # Research task
        tasks.append(Task(
            description=(
                'Analyze production and market data to identify: \n'
                '1. Production efficiency metrics\n'
                '2. Cost optimization opportunities\n'
                '3. Market share analysis\n'
                '4. Supply chain optimization\n'
                '5. Technology adoption and modernization needs'
            ),
            agent=self.agents['researcher']
        ))
        
        # Analysis task
        tasks.append(Task(
            description=(
                'Generate strategic recommendations focusing on: \n'
                '1. Production capacity optimization\n'
                '2. Market positioning and competitive advantage\n'
                '3. Cost reduction strategies\n'
                '4. Growth opportunities and expansion plans\n'
                '5. Sustainability and environmental compliance'
            ),
            agent=self.agents['analyst']
        ))
        
        return tasks

    def _create_crew(self):
        """Create the CREW AI crew"""
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=2,
            process=Process.sequential
        )

    def run_crew(self, company="JSW Steel", project="Steel Production Analysis", keywords=None):
        """Execute the crew's tasks"""
        try:
            # Get MCP data
            mcp_data = self.composio.get_mcp_data()
            formatted_mcp_data = format_mcp_data(mcp_data)
            
            # Set context for the crew
            context = {
                'company': company,
                'project': project,
                'mcp_data': formatted_mcp_data,
                'keywords': keywords or [
                    f"{company} production",
                    f"{company} expansion",
                    "steel market trends",
                    "steel industry analysis"
                ],
                'industry_focus': {
                    'sector': 'Steel Manufacturing',
                    'key_metrics': [
                        'Production Capacity',
                        'Capacity Utilization',
                        'Raw Material Costs',
                        'Energy Efficiency',
                        'Environmental Compliance'
                    ]
                }
            }
            
            # Run the crew with context
            result = self.crew.kickoff(context=context)
            
            # Process and save results
            final_results = {
                'mcp_analysis': formatted_mcp_data,
                'crew_analysis': result,
                'metadata': {
                    'company': company,
                    'project': project,
                    'timestamp': formatted_mcp_data.get('timestamp'),
                    'industry': 'Steel Manufacturing',
                    'analysis_focus': 'Production and Market Analysis'
                }
            }
            
            # Save results
            save_results(final_results)
            
            return final_results
        except Exception as e:
            logger.error(f"Error running crew: {str(e)}")
            raise 