"""
API client for Cloudflare Workers
"""

import requests
import logging
from typing import Dict, Optional
from app.config import Config

logger = logging.getLogger(__name__)


def fetch_config(params: Dict[str, str]) -> Optional[str]:
    """
    Fetch VPN config from Cloudflare Workers API
    
    Args:
        params: Query parameters (cc, vpn, port, limit, format)
    
    Returns:
        Config string or None if error
    """
    try:
        api_url = Config.get_api_url()
        
        logger.info(f"Fetching config: {params}")
        
        response = requests.get(
            api_url,
            params=params,
            timeout=Config.API_TIMEOUT
        )
        
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
        
        config = response.text
        
        logger.info(f"Config fetched successfully: {len(config)} bytes")
        
        return config
        
    except requests.Timeout:
        logger.error("API request timeout")
        return None
        
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
