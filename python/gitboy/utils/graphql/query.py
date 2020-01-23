from typing import Optional, List
from .core import BaseQuery
from .constants import *

def get_last_cursor(edges:List[dict]):
    """
    Function to get the last cursor of the edges in a response
    """
    if len(edges) > 0:
        return edges[-1].get("cursor")

    return None

class RepositoryFetchQuery(BaseQuery):
    def __init__(self, variables:Optional[dict] = None):
        super().__init__(variables)
        self.query = FETCH_REPOS

    def process_response(self, response: dict):
        _response = {"_raw": response}
        watching = response.get("data", {}).get("viewer", {}).get("watching", {})
        edges = watching.get("edges", [])

        def edge_to_data(edge: dict):
            node = edge.get("node", {})
            _data = {
                "id": node.get("id"),
                "name": node.get("name"),
                "owner": node.get("owner", {}).get("login")
            }
            return _data

        
        _response['totalCount'] = watching.get("totalCount")
        _response['data'] = [edge_to_data(e) for e in edges]
        _response['lastCursor'] = get_last_cursor(edges)

        return _response
