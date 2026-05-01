import os
from typing import Dict, Any, Optional

import requests
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class USDAFASClient:
    """
    Client for the USDA FAS Open Data API.
    """
    BASE_URL = "https://api.fas.usda.gov"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the client.

        Args:
            api_key (str, optional): The API key. If not provided, looks for USDA_FAS_API_KEY env var.
            timeout (int, optional): Request timeout in seconds.
            base_url (str, optional): Override the default API host.
        """
        self.api_key = api_key or os.getenv("USDA_FAS_API_KEY")
        self.timeout = timeout
        self.base_url = base_url or self.BASE_URL

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
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
