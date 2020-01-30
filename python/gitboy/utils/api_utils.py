"""
File containing utilities to serve as interface to the Github APIs.
Refer: https://developer.github.com/v3/
"""
from typing import Optional

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

    def get_logged_in_user(self):
        query = gql_query.LoggedInUserFetchQuery()
        _response = self._client.process(query)
        if _response["data"] is None:
            return None

        return _response["data"].get("login")

    def get_user_repos(self):
        cursor = ""
        data = []
        while True:
            query = gql_query.RepositoryFetchQuery(variables={"cursor": cursor})
            _response = self._client.process(query)
            if None in [_response["totalCount"], _response["data"]]:
                break

            data.extend(_response["data"])

            cursor = _response["lastCursor"]

            if cursor is None:
                # exit loop once pagination loop completes
                break

        return data

    def get_repo_issues(self, repo_name: str, repo_owner: str):
        cursor = ""
        data = []
        while True:
            query = gql_query.RepositoryIssuesFetchQuery(
                variables={"repoName": repo_name, "repoOwner": repo_owner, "cursor": cursor}
            )
            _response = self._client.process(query)
            if None in [_response["totalCount"], _response["data"]]:
                break

            data.extend(_response["data"])

            cursor = _response["lastCursor"]

            if cursor is None:
                # exit loop once pagination loop completes
                break

        return data

    def get_all_issues(self):
        """
        Function to get all issues a user has access to.
        Process:
          1. Get all repos he has access to
          2. Fetch issues per repo
        """
        repos = self.get_user_repos()
        issues = []

        for r in repos:
            issues.extend(self.get_repo_issues(repo_name=r["name"], repo_owner=r["owner"]))

        return issues
