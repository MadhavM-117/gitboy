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
		
		self._base_url = "https://api.github.com/"
		self._config = config
		self.token = config.token
		self.organization = config.organization

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

		response = get_issues_req.json()

		return [f"{i['html_url']} - f{i['title']}" for i in response]
		
