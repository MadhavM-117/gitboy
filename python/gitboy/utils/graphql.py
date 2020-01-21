"""
Module to help handle GraphQL API calls
"""
import requests

class GraphQLClient:
	def __init__(self, base_url, auth=None, auth_header="Authorization"):
		self.base_url = base_url
		self.auth_header_val = auth
		self.auth_header = auth_header

	def process(self, query, variables=None):
		_body = {"query": query, "variables": variables}
		headers = {}
		if self.auth_header_val:
			headers[self.auth_header] = self.auth_header_val

		req = requests.post(self.base_url, json=_body, headers=headers)
		req.raise_for_status()

		return req.json()
