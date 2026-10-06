"""Module with functionalities and classes to interact with Alpha Vantage
API
"""

# External libraries
from typing import Any, Literal

import requests


class AlphaVantageAPI:
    """Class to interact with Alpha Vantage API
    """

    FUNCTIONS = {
        "GLOBAL_QUOTE": "GLOBAL_QUOTE",
        "INCOME_STATEMENT": "INCOME_STATEMENT",
        "BALANCE_SHEET": "BALANCE_SHEET",
        "CASH_FLOW": "CASH_FLOW",
        "NEWS_SENTIMENT": "NEWS_SENTIMENT",
    }
    """Functions dictionary which can be executed in Alpha Vantage API"""

    def __init__(self, api_key: str) -> None:
        """Initializator Alpha Vantage API

        Args:
            api_key: api key to authenticate in Alpha Vantage API
        """
        self.url = "https://www.alphavantage.co"
        self.api_key = api_key

    def _set_apikey(self, query_parameters: dict[str, Any]):
        """Add apikey in parameters to use in queries"""

        # Avoid modify original dictionary
        return {
            **query_parameters,
            "apikey": self.api_key,
        }

    def _query(
        self, query_parameters: dict[str, Any], timeout: float = 30
    ) -> dict:
        """Perform a query based in parameters given"""

        query_parameters_aux = self._set_apikey(query_parameters=query_parameters)
        request = requests.get(
            url=f"{self.url}/query",
            params=query_parameters_aux,
            timeout=timeout
        )
        request.raise_for_status()
        return request.json()

    def global_quote(
        self,
        symbol: str,
        datatype: Literal["json", "csv"] = "json",
        entitlement: Literal["realtime", "delayed"] | None = None,
        timeout: float = 30,
    ) -> dict:
        """Get latest price and volume information about a specific ticker

        Based on https://www.alphavantage.co/documentation/#latestprice

        Args:
            symbol: The symbol of the global ticker of your choice.
                For example: symbol=IBM.
            datatype: Return information in json or csv (comma separated). By
                default "json"
            entitlement: Controls the market data entitlement. "realtime" returns
                realtime US market data, while "delayed" returns 15-minute
                delayed data.
            timeout: Max time to wait for an API response.

        Returns:
            Dictionary with data getted about a ticker given.

        Raises:
            HTTPError: If HTTP status erro code ocurred (400 - 599 status code)
            ReadTimeout: If API takes a long time returning a response
        """

        parameters = {
            "function": self.FUNCTIONS["GLOBAL_QUOTE"],
            "symbol": symbol,
            "datatype": datatype,
        }
        if entitlement is not None:
            parameters["entitlement"] = entitlement
        return self._query(parameters, timeout=timeout)
