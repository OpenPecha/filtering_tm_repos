import base64
import re

from repo_filter.list_repo import authenticate_github, get_tm_repo_list, write_file


def find_date_mentions_in_repo(repo, date_patterns):
    """
    Find date mentions in a GitHub repository's text files.

    Args:
        repo (Repository): PyGithub Repository object.
        date_patterns (list): List of regular expression patterns for date matching.

    Returns:
        bool: True if date mentions are found, False otherwise.
    """
    try:
        for file in repo.get_contents(""):
            if file.name.lower().endswith(".txt") and "en" in file.name.lower():
                try:
                    # Fetch the raw content of the text file
                    file_content_base64 = file.content

                    # Decode the base64 content
                    file_content = base64.b64decode(file_content_base64).decode(
                        "utf-8", errors="ignore"
                    )

                    for pattern in date_patterns:
                        dates_found = re.findall(pattern, file_content)
                        if dates_found:
                            return True
                except UnicodeDecodeError:
                    print(f"Error decoding {file.name}: UnicodeDecodeError")
    except Exception as e:
        if "This repository is empty." in str(e):
            pass  # Ignore empty repository error
        else:
            print(f"Error accessing repository: {e}")
    return False


def get_date_patterns():
    patterns = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD, YYYY-DD-MM
        r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY, DD/MM/YYYY
        r"\d{4}/\d{2}/\d{2}",  # YYYY/DD/MM, YYYY/MM/DD
        r"\d{2}-\d{2}-\d{4}",  # DD-MM-YYYY, MM-DD-YYYY
        r"\d{4}",  # YYYY just year
        # Add more date formats as needed
    ]
    return patterns


def filter_repositories_with_dates(org_name, token, filepath):
    """
    Filter repositories in an organization for date mentions in text files.

    Args:
        org_name (str): GitHub organization name.
        token (str): GitHub personal access token.

    Returns:
        list: List of repository names with date mentions.
    """
    github = authenticate_github(token)
    org = github.get_organization(org_name)

    date_patterns = get_date_patterns()
    repos_with_dates = []

    tm_repos = get_tm_repo_list(filepath)

    for tm_repo in tm_repos:
        repo = org.get_repo(tm_repo)
        if find_date_mentions_in_repo(repo, date_patterns):
            repos_with_dates.append(repo.name)

    return repos_with_dates


if __name__ == "__main__":
    # Replace with your GitHub organization name and personal access token
    org_name = "MonlamAI"
    token = "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"
    filepath = "list.txt"
    filewrite = "date_repo.txt"

    # Get repositories with date mentions
    repos_with_dates = filter_repositories_with_dates(org_name, token, filepath)

    write_file(repos_with_dates, filewrite)

    # Print the list of repositories with date mentions
    print("Repositories containing date mentions:")
    for repo_name in repos_with_dates:
        print(repo_name)
