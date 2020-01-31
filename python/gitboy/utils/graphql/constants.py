FETCH_LOGGED_IN_USER = """
query {
  viewer {
    login
  }
}
"""

FETCH_REPOS = """
query($cursor:String) {
  viewer {
    watching(first:10, orderBy:{field:CREATED_AT, direction:DESC}, after:$cursor) {
      totalCount
      edges {
        node {
          id
          name
          owner {
            login
          }
        }
        cursor
      }
    }
  }
}
"""

FETCH_ISSUES_IN_REPO = """
query($repoName:String!, $repoOwner:String!, $cursor:String) {
  repository(name:$repoName, owner:$repoOwner) {
    name
    issues(first:100, orderBy:{field:UPDATED_AT, direction:DESC}, after:$cursor) {
      totalCount
      edges {
        node {
          title
          url
          updatedAt
        }
        cursor
      }
    }
  }
}

"""

# @TODO: Figure out a query to fetch all issues, even if multiple requests are needed for pagination.
# @TODO: Figure out how to combine requests to fetch all objects.
