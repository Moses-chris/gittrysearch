# ranking_system.py

def calculate_rank(stars, recent_activity, forks, contributors):
    # Simple weighted scoring system
    score = (
        stars * 0.5 +
        recent_activity * 0.2 +
        forks * 0.2 +
        contributors * 0.1
    )
    return score

def rank_repositories(repos):
    # Assuming repos is a list of dictionaries with necessary information
    for repo in repos:
        repo['rank'] = calculate_rank(
            repo['stars'],
            repo['recent_activity'],
            repo['forks'],
            repo['contributors']
        )
    
    # Sort repos by rank in descending order
    ranked_repos = sorted(repos, key=lambda x: x['rank'], reverse=True)
    return ranked_repos

if __name__ == "__main__":
    # Example usage
    sample_repos = [
        {"name": "repo1", "stars": 1000, "recent_activity": 100, "forks": 200, "contributors": 50},
        {"name": "repo2", "stars": 2000, "recent_activity": 50, "forks": 100, "contributors": 30},
    ]
    ranked = rank_repositories(sample_repos)
    for repo in ranked:
        print(f"{repo['name']}: Rank {repo['rank']}")