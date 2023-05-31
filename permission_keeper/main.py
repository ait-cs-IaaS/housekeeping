from github import Github, GithubException, Team, Repository
from typing import List

# first, we're going to need a Github instance
# usually, we'd use a token for this, but we're just using a placeholder here
# replace 'your-token' with your actual GitHub access token
g = Github('your-token')

def ensure_team_in_repo(team: Team, repo: Repository, permission: str='push'):
    try:
        team_repo_permission = team.get_repo_permission(repo)
        if team_repo_permission is None or team_repo_permission.permission != permission:
            team.set_repo_permission(repo, permission)
    except GithubException as e:
        print(f"Error: {e}")

def ensure_team_in_all_repos(g: Github, org_name: str, team_name: str, permission: str='push'):
    org = g.get_organization(org_name)
    team = None
    try:
        team = org.get_team_by_slug(team_name)
    except GithubException:
        team = org.create_team(team_name, [org.default_repository_permission], org.default_repository_privacy)

    repos: List[Repository] = org.get_repos()

    for repo in repos:
        ensure_team_in_repo(team, repo, permission)

if __name__ == '__main__':
    ensure_team_in_all_repos(g, 'ait-cs-IaaS', 'CyberRangers', 'push')

