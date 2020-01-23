FETCH_USER_ISSUES = """
query {
	viewer {
		issues(orderBy:{direction:DESC, field:UPDATED_AT}, filterBy:{states:[OPEN]}, first:10) {
			totalCount
			nodes {
				title
				url
			}
		}
	}
}
"""

FETCH_ALL_ISSUES_THROUGH_REPOS = """
query {
	viewer {
    watching(first:100, orderBy:{field:UPDATED_AT, direction:DESC}) {
      totalCount
      nodes {
        name
        issues(first:100, orderBy:{field:UPDATED_AT, direction:DESC} ,filterBy:{states:[OPEN, CLOSED]}) {
          totalCount
          nodes {
            title
            url
            updatedAt
          }
        }
      }
    }
  }
}
"""

FETCH_REPOS = """
query($repoCursor:String) {
  viewer {
    watching(first:100, orderBy:{field:CREATED_AT, direction:DESC}, after:$repoCursor) {
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

# @TODO: Figure out a query to fetch all issues, even if multiple requests are needed for pagination. 
# @TODO: Figure out how to combine requests to fetch all objects.  