"""
File containing utilities to serve as interface to the Github APIs. 
Refer: https://developer.github.com/v3/
"""
from typing import Optional

import requests
from .config import get_config, Config

class GithubAPIs:
	def __init__(self, config: Optional[Config] = None):
		if config is None:
			config = get_config()
		
		self._base_url = "https://api.github.com"
		self._config = config
		self.token = config.token
		self.organization = config.organization

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

	def get_issues(self, _filter: str = "assigned"):
		"""
		Function to get issues using the specified filter
		Args:
			_filter: Filter to use while fetching the issues. Default: 'assigned'
							 One of ['assigned', 'created', 'mentioned', 'subscribed', 'all']
		"""
		issues_url = f"{self._base_url}"
 
		if self.organization is not None:
			issues_url += f"/orgs/{self.organization}"

		issues_url += "/issues"

		get_issues_req = requests.get(issues_url, headers={
			"Accept": "application/vnd.github.v3+json",
			"Authorization": f"token {self.token.strip()}"
		}, params={
			"filter": _filter,
			"sort": "updated"
		})

		get_issues_req.raise_for_status()

		issues = []
		issues.extend(list(get_issues_req.json()))

		next_req = get_issues_req

		while self.get_next_pagination_link(next_req.headers.get('Link')) is not None:
			next_url = self.get_next_pagination_link(next_req.headers.get('Link'))
			next_req = requests.get(next_url, headers={
				"Accept": "application/vnd.github.v3+json",
				"Authorization": f"token {self.token.strip()}"
			})
			next_req.raise_for_status()
			issues.extend(list(next_req.json()))

		return [f"{i['title']} - {i['html_url']}" for i in issues]
		
