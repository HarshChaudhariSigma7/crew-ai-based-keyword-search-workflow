# CREW AI Steel Industry Analyzer

This project integrates CREW AI with Composio MCP to perform automated analysis of steel industry data, with a focus on JSW Steel.

## Project Structure

```
.
├── app.py                # Flask web application
├── templates/            # HTML templates
│   └── index.html        # Web interface
├── config/               # Configuration files
│   └── config.py         # Environment variables and settings
├── src/                  # Core application code
│   ├── main.py           # CLI entry point
│   ├── composio_api.py   # Composio MCP API client
│   └── crew_agents.py    # CREW AI agents and tasks
├── utils/                # Utility modules
│   ├── helpers.py        # Helper functions
│   ├── search_api.py     # Google search functionality
│   └── scraper.py        # Web scraping functionality
├── requirements.txt      # Project dependencies
└── .env                  # Environment variables (not tracked in git)
```

## Data Flow Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Web UI     │────▶│  Flask API  │────▶│  CREW AI    │
│ (Browser)   │◀────│  (app.py)   │◀────│  Engine     │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Results    │◀────│  Analysis   │◀────│  Data       │
│  Display    │     │  Processing │     │  Collection │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ External    │
                                        │ APIs        │
                                        │ - Composio  │
                                        │ - Serper    │
                                        │ - Firecrawl │
                                        └─────────────┘
```

### Data Flow Process

1. **User Input**: User enters company name and analysis type in the web interface
2. **Request Processing**: Flask API receives the request and initiates background analysis
3. **Agent Initialization**: CREW AI agents are initialized with specific roles
4. **Data Collection**:
   - Composio MCP data is retrieved
   - Web search is performed via Serper API
   - Relevant web content is scraped via Firecrawl API
5. **Analysis**:
   - Researcher agent analyzes combined data
   - Analyst agent generates recommendations
6. **Result Processing**: Results are structured and categorized
7. **Response**: Results are sent back to the web interface
8. **Display**: User sees analysis results in tabbed interface

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your environment variables:
   - Copy `.env.example` to `.env` (if it doesn't exist)
   - Add your Composio API key
   - Add your Groq API key
   - Add your Serper API key (for web search)
   - Add your Firecrawl API key (for web scraping)

## Usage

### Web Interface

Run the Flask web application:
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The web interface allows you to:
- Specify a company to analyze (default: JSW Steel)
- Choose an analysis type
- View results in different categories (Summary, Production, Market, Recommendations)

### Command Line

You can also run the analysis directly from the command line:
```bash
python -m src.main --company "JSW Steel" --project "Steel Production Analysis"
```

## Features

- **Web Interface**: User-friendly interface for running analyses
- **Real-time Status Updates**: Track analysis progress
- **Multiple Analysis Types**: Comprehensive, Production, Market, or Competitor analysis
- **Tabbed Results View**: Organized presentation of findings
- **Key Metrics**: Production capacity, market share, and efficiency ratings
- **Detailed Recommendations**: Strategic insights for business improvement

## Requirements

- Python 3.8+
- Composio MCP API access
- Groq API key
- Serper API key (for web search)
- Firecrawl API key (for web scraping)

## Developer Notes

### Important Implementation Details

1. **API Key Management**:
   - All API keys are loaded from `.env` file
   - Never commit `.env` file to version control
   - Use environment variables in production environments

2. **CREW AI Configuration**:
   - Agent roles are defined in `config.py`
   - Task descriptions are in `crew_agents.py`
   - Modify these to adjust agent behavior

3. **Error Handling**:
   - API failures are gracefully handled
   - Check logs for detailed error information
   - Web interface shows user-friendly error messages

4. **Performance Considerations**:
   - Analysis runs in background threads to prevent blocking
   - Long-running analyses (>5 minutes) may time out in some environments
   - Consider implementing a job queue for production

5. **Extending the System**:
   - Add new agents in `crew_agents.py`
   - Add new API integrations in `utils/`
   - Add new metrics in `process_results()` in `app.py`

### Common Issues and Solutions

1. **API Rate Limiting**:
   - Serper API has rate limits - implement caching for frequent searches
   - Groq may have token limits - adjust max_tokens parameter if needed

2. **Memory Usage**:
   - Large analyses may consume significant memory
   - Monitor memory usage and implement pagination for large datasets

3. **Timeout Handling**:
   - Web requests may timeout for long-running analyses
   - Implement a polling mechanism with longer timeouts

4. **Model Versioning**:
   - Groq models may change - update GROQ_MODEL in config.py if needed
   - Test with new model versions before deploying

## Development

To run tests:
```bash
python -m unittest discover tests
```

To add a new analysis type:
1. Add the type to the dropdown in `templates/index.html`
2. Add processing logic in `process_results()` in `app.py`
3. Add corresponding task in `crew_agents.py` 