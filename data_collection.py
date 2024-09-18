# data_collection.py

import requests
import os
from datetime import datetime, timedelta

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_top_repos(min_stars=1000, last_update=None):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    query = f"""
    query {{
      search(query: "stars:>={min_stars} sort:stars-desc", type: REPOSITORY, first: 100) {{
        edges {{
          node {{
            ... on Repository {{
              name
              description
              stargazerCount
              primaryLanguage {{
                name
              }}
              repositoryTopics(first: 10) {{
                nodes {{
                  topic {{
                    name
                  }}
                }}
              }}
              updatedAt
            }}
          }}
        }}
      }}
    }}
    """
    
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        return [repo["node"] for repo in data["data"]["search"]["edges"]]
    else:
        raise Exception(f"Query failed with status code: {response.status_code}")

if __name__ == "__main__":
    repos = fetch_top_repos()
    print(f"Fetched {len(repos)} repositories")