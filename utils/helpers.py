import json
import logging

logger = logging.getLogger(__name__)

def format_mcp_data(data):
    """
    Format MCP data for analysis
    
    Args:
        data (dict): Raw MCP data
        
    Returns:
        dict: Formatted data
    """
    try:
        return {
            'timestamp': data.get('timestamp'),
            'metrics': data.get('metrics', {}),
            'status': data.get('status'),
            'formatted_time': format_timestamp(data.get('timestamp'))
        }
    except Exception as e:
        logger.error(f"Error formatting MCP data: {str(e)}")
        raise

def format_timestamp(timestamp):
    """
    Format timestamp to human-readable format
    
    Args:
        timestamp (int): Unix timestamp
        
    Returns:
        str: Formatted timestamp
    """
    from datetime import datetime
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logger.error(f"Error formatting timestamp: {str(e)}")
        return None

def save_results(results, filename='analysis_results.json'):
    """
    Save analysis results to file
    
    Args:
        results (dict): Analysis results
        filename (str): Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        raise 