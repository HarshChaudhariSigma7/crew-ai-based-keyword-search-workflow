from flask import Flask, render_template, request, jsonify
import os
import json
import logging
import subprocess
import threading
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store analysis results
analysis_results = {}
analysis_status = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    data = request.json
    company = data.get('company', 'JSW Steel')
    project = data.get('project', 'Steel Production Analysis')
    analysis_type = data.get('analysisType', 'comprehensive')
    
    # Generate a unique ID for this analysis
    analysis_id = f"{company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Set initial status
    analysis_status[analysis_id] = 'running'
    
    # Start analysis in background thread
    thread = threading.Thread(
        target=run_analysis_thread,
        args=(analysis_id, company, project, analysis_type)
    )
    thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Analysis started',
        'analysisId': analysis_id
    })

@app.route('/api/analysis-status/<analysis_id>', methods=['GET'])
def get_analysis_status(analysis_id):
    status = analysis_status.get(analysis_id, 'not_found')
    
    if status == 'completed' and analysis_id in analysis_results:
        return jsonify({
            'status': status,
            'results': analysis_results[analysis_id]
        })
    
    return jsonify({
        'status': status
    })

def run_analysis_thread(analysis_id, company, project, analysis_type):
    try:
        logger.info(f"Starting analysis for {company} - {project}")
        
        # Build command to run the analysis
        cmd = [
            'python', '-m', 'src.main',
            '--company', company,
            '--project', project
        ]
        
        # Run the command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logger.error(f"Analysis failed: {stderr}")
            analysis_status[analysis_id] = 'failed'
            return
        
        # Try to load results from the JSON file
        try:
            with open('analysis_results.json', 'r') as f:
                results = json.load(f)
                
            # Process results based on analysis type
            processed_results = process_results(results, analysis_type)
            
            # Store results
            analysis_results[analysis_id] = processed_results
            analysis_status[analysis_id] = 'completed'
            
            logger.info(f"Analysis completed for {company}")
            
        except Exception as e:
            logger.error(f"Error processing results: {str(e)}")
            analysis_status[analysis_id] = 'failed'
            
    except Exception as e:
        logger.error(f"Error running analysis: {str(e)}")
        analysis_status[analysis_id] = 'failed'

def process_results(results, analysis_type):
    """Process and format the analysis results based on the analysis type"""
    
    # Extract the crew analysis text
    crew_analysis = results.get('crew_analysis', '')
    
    # Create a structured response
    processed = {
        'summary': extract_section(crew_analysis, 'summary'),
        'production': extract_section(crew_analysis, 'production'),
        'market': extract_section(crew_analysis, 'market'),
        'recommendations': extract_section(crew_analysis, 'recommendations'),
        'metrics': {
            'production_capacity': extract_metric(crew_analysis, 'production capacity'),
            'market_share': extract_metric(crew_analysis, 'market share'),
            'efficiency_rating': extract_metric(crew_analysis, 'efficiency')
        }
    }
    
    return processed

def extract_section(text, section_type):
    """Extract a specific section from the analysis text"""
    # This is a simple implementation - in a real app, you'd use more sophisticated parsing
    if section_type == 'summary':
        return text[:500] if len(text) > 500 else text
    
    # Look for keywords related to each section
    section_keywords = {
        'production': ['production', 'capacity', 'plant', 'manufacturing'],
        'market': ['market', 'share', 'competitor', 'industry', 'demand'],
        'recommendations': ['recommend', 'strategy', 'should', 'could', 'opportunity']
    }
    
    # Find paragraphs containing the keywords
    paragraphs = text.split('\n\n')
    matching_paragraphs = []
    
    for paragraph in paragraphs:
        if any(keyword in paragraph.lower() for keyword in section_keywords.get(section_type, [])):
            matching_paragraphs.append(paragraph)
    
    return '\n\n'.join(matching_paragraphs) if matching_paragraphs else "No specific information available."

def extract_metric(text, metric_type):
    """Extract a specific metric from the analysis text"""
    # This is a simplified implementation
    if metric_type == 'production capacity':
        # Look for patterns like "X MTPA" or "X million tonnes"
        if 'MTPA' in text:
            return '18.5 MTPA'  # Placeholder
        return 'Not available'
    
    elif metric_type == 'market share':
        # Look for patterns like "X% market share"
        return '21.3%'  # Placeholder
    
    elif metric_type == 'efficiency':
        return '76/100'  # Placeholder
    
    return 'Not available'

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000) 