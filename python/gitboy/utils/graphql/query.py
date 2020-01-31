from typing import Optional, List

from dateutil.parser import parse

from .core import BaseQuery
from . import constants


def get_last_cursor(edges: List[dict]):
    """
    Function to get the last cursor of the edges in a response
    """
    if len(edges) > 0:
        return edges[-1].get("cursor")

    return None


class LoggedInUserFetchQuery(BaseQuery):
    def __init__(self, variables: Optional[dict] = None):
        super().__init__(variables)
        self.query = constants.FETCH_LOGGED_IN_USER

    def process_response(self, response):
        _response = {"_raw": response}
        _response["data"] = {"login": response.get("data", {}).get("viewer", {}).get("login")}
        return _response


class RepositoryFetchQuery(BaseQuery):
    def __init__(self, variables: Optional[dict] = None):
        super().__init__(variables)
        self.query = constants.FETCH_REPOS

    def process_response(self, response: dict):
        _response = {"_raw": response}
        watching = response.get("data", {}).get("viewer", {}).get("watching", {})
        edges = watching.get("edges", [])

        def edge_to_data(edge: dict):
            node = edge.get("node", {})
            _data = {"id": node.get("id"), "name": node.get("name"), "owner": node.get("owner", {}).get("login")}
            return _data

        _response["totalCount"] = watching.get("totalCount")
        _response["data"] = [edge_to_data(e) for e in edges]
        _response["lastCursor"] = get_last_cursor(edges)

        return _response


class RepositoryIssuesFetchQuery(BaseQuery):
    def __init__(self, variables: Optional[dict] = None):
        if variables is None:
            raise ValueError("Expected variables that define a repository.")

        if None in [variables.get("repoName"), variables.get("repoOwner")]:
            raise ValueError("Repository Name / Owner missing.")

        super().__init__(variables)
        self.query = constants.FETCH_ISSUES_IN_REPO

    def process_response(self, response: dict):
        _response = {"_raw": response}
        issues = response.get("data", {}).get("repository", {}).get("issues", {})
        edges = issues.get("edges") or []

        def edge_to_data(edge: dict):
            node = edge.get("node", {})
            _data = {
                "title": node.get("title"),
                "url": node.get("url"),
                "updatedAt": node.get("updatedAt") and parse(node["updatedAt"]),
            }
            return _data

        _response["totalCount"] = issues.get("totalCount")
        _response["data"] = [edge_to_data(e) for e in edges]
        _response["lastCursor"] = get_last_cursor(edges)

        return _response
