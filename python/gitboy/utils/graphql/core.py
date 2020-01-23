"""
Module to help handle GraphQL API calls
"""
from abc import ABC, abstractmethod
from typing import Optional

import requests

class BaseQuery(ABC):
    def __init__(self, variables:Optional[dict] = None):
        self.query = None
        self.variables = variables

    @abstractmethod
    def process_response(self, response:dict) -> dict:
        """
        Function to get the appropriate values from the API response
        """
        raise NotImplementedError

class GraphQLClient:
	def __init__(self, base_url, auth=None, auth_header="Authorization"):
		self.base_url = base_url
		self.auth_header_val = auth
		self.auth_header = auth_header

	def process(self, query:BaseQuery):
		_body = {"query": query.query, "variables": query.variables}
		headers = {}
		if self.auth_header_val:
			headers[self.auth_header] = self.auth_header_val

		req = requests.post(self.base_url, json=_body, headers=headers)
		req.raise_for_status()

		return query.process_response(req.json())


