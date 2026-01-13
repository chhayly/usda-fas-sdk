import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables from .env file if present
load_dotenv()

class USDAFASClient:
    """
    Client for the USDA FAS Open Data API.
    """
    BASE_URL = "https://api.fas.usda.gov"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the client.

        Args:
            api_key (str, optional): The API key. If not provided, looks for USDA_FAS_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("USDA_FAS_API_KEY")
        
        if not self.api_key:
            raise ValueError("API Key is required. Provide it in __init__ or set USDA_FAS_API_KEY in environment/.env")
            
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": self.api_key,
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Internal method to make requests to the API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint (e.g., /api/esr/regions)
            params (Optional[Dict[str, Any]]): Query parameters.

        Returns:
            Any: The JSON response from the API.

        Raises:
            requests.HTTPError: If the request fails.
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, params=params)
        response.raise_for_status()
        return response.json()
