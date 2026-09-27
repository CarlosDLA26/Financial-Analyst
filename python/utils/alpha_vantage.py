# External libraries
from typing import Any

import requests


class AlphaVantageAPI:

    FUNCTIONS = []

    def __init__(self, api_key: str):
        """"""
        self.url = "https://www.alphavantage.co"
        self.api_key = api_key

    @staticmethod
    def _create_url_query_parameter(query_parameters: dict[str, Any]) -> str:
        """Create part in URL to query data"""

        list_strs = [f"{k}={v}" for k, v in query_parameters.items()]
        return "&".join(list_strs)

    def _set_apikey(self, query_parameters: dict[str, Any]):
        """Add apikey in parameters to use in queries"""

        query_parameters["apikey"] = self.api_key
        return query_parameters

    def query(self, query_parameters: dict[str, Any]) -> dict:
        """Perform a query based in parameters given"""

        query_parameters_aux = self._set_apikey(query_parameters=query_parameters)
        parameters = AlphaVantageAPI._create_url_query_parameter(
            query_parameters=query_parameters_aux
        )
        url = f"{self.url}/query?{parameters}"
        request = requests.get(url=url)
        request. raise_for_status()
        return request.json()
