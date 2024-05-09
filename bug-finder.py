import argparse
import re
from git import Repo
import os

def get_repo_name(repo_url):
    return repo_url.split('/')[-1].rstrip('.git')

def clone_repo(repo_url, depth, bare=False):
    repo_name = get_repo_name(repo_url)
    repo_path = os.path.join('cloned_repos', repo_name)

    if not os.path.isdir(repo_path) or not os.listdir(repo_path):
        print(f"Cloning repository from {repo_url} with depth {depth} into {repo_path}...")
        Repo.clone_from(repo_url, repo_path, depth=depth, bare=bare)
    else:
        print(f"{repo_path} already exists. Using existing directory.")
    return repo_path

def search_commits(repo_url, repo_path, pattern):
    repo = Repo(repo_path, search_parent_directories=True)
    compiled_pattern = re.compile(pattern)

    print(f"Searching for commits that match the pattern {pattern}")
    commits_list = list(repo.iter_commits())
    for i, commit in enumerate(commits_list):
        if compiled_pattern.search(commit.message):
            print(f'Commit {commit.hexsha}: {commit.summary}')
            print(f'Date: {commit.authored_datetime}')
            print(f'Message: {commit.message}')
            if i + 1 < len(commits_list):
                previous_commit = commits_list[i + 1]
                repo_name = get_repo_name(repo_url)
                print(f"To checkout this commit run:")
                print(f"git clone --single-branch {repo_url} {repo_name} && cd {repo_name} && git checkout {previous_commit.hexsha}")
            print('-----------------------------------')

parser = argparse.ArgumentParser(description="Search Git commits for specific patterns to try and find bugs.")
parser.add_argument('repo_url', type=str, help="URL of the Git repository to clone.")
parser.add_argument('--depth', type=int, default=100, help="Depth of the repository history to clone.")
parser.add_argument('--pattern', type=str, default=r'#[0-9]+', help="Regex pattern to search in commit messages.")

args = parser.parse_args()
repo_path = clone_repo(args.repo_url, args.depth)
search_commits(args.repo_url, repo_path, args.pattern)
