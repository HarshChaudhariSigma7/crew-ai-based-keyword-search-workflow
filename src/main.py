from src.crew_agents import CrewAgents
from src.composio_api import ComposioAPI
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    'company': 'JSW Steel',
    'project': 'Steel Production Analysis',
    'keywords': ['steel production', 'iron ore', 'steel market', 'JSW expansion']
}

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run CREW AI analysis with Composio MCP')
    parser.add_argument('--company', type=str, default=DEFAULT_CONFIG['company'],
                      help=f'Company name to analyze (default: {DEFAULT_CONFIG["company"]})')
    parser.add_argument('--project', type=str, default=DEFAULT_CONFIG['project'],
                      help=f'Project name to analyze (default: {DEFAULT_CONFIG["project"]})')
    args = parser.parse_args()

    try:
        # Initialize CrewAgents
        logger.info(f"Initializing CREW AI agents for {args.company}...")
        crew_agents = CrewAgents()
        
        # Run the crew
        logger.info(f"Starting crew execution for {args.company} - {args.project}...")
        result = crew_agents.run_crew(
            company=args.company,
            project=args.project,
            keywords=DEFAULT_CONFIG['keywords'] if args.company == DEFAULT_CONFIG['company'] else None
        )
        
        # Print results
        logger.info("Crew execution completed successfully")
        print("\nCrew AI Analysis Results:")
        print("-------------------------")
        print(f"Company: {args.company}")
        print(f"Project: {args.project}")
        print("-------------------------")
        if isinstance(result, dict) and 'crew_analysis' in result:
            print(result['crew_analysis'])
        else:
            print(result)
        print("\nResults have been saved to analysis_results.json")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 