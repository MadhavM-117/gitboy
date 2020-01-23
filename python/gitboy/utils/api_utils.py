"""
File containing utilities to serve as interface to the Github APIs. 
Refer: https://developer.github.com/v3/
"""
from typing import Optional

import requests
from .config import get_config, Config
from .graphql.core import GraphQLClient
from .graphql import query as gql_query

class GithubAPIs:
	def __init__(self, config: Optional[Config] = None):
		if config is None:
			config = get_config()
		
		self._base_url = "https://api.github.com/graphql"
		self._config = config
		self.token = config.token
		self.organization = config.organization
		self._client = GraphQLClient(self._base_url, auth=f"bearer {self.token}")

	@staticmethod
	def get_next_pagination_link(link_header: str):
		"""
		Function to get the next pagination link as per Github's API structure
		"""
		if link_header is None:
			return None

		links = link_header.split(',')
		for link in links:
			values = link.split(';')
			if values[1].endswith('rel="next"'):
				return values[0].replace('<', '').replace('>', '')
		
		return None

	def get_user_repos(self):
		cursor = ""
		data = []
		while True:
			query = gql_query.RepositoryFetchQuery(variables={"cursor": cursor})
			_response = self._client.process(query)
			if None in [_response['totalCount'], _response['lastCursor'], _response['data']]:
				break

			data.extend(_response['data'])

			if len(data) >= _response['totalCount']:
				# exit loop once pagination loop completes
				break

			cursor = _response['lastCursor']

		return data