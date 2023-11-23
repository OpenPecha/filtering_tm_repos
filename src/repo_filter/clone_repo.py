import base64
import json
import re

from repo_filter.list_repo import authenticate_github
from repo_filter.testing import get_tm_repo_list


def write_to_file(data, filename):
    """
    Write list items to a file, each on a new line.

    Args:
        data (list of str): Content to write.
        filename (str): Target file path.

    Note: Doesn't return a value.
    """
    with open(filename, "w") as my_file:
        for line in data:
            my_file.write(line + "\n")  # The '\n' is a newline character


def find_date_mentions_in_repo(repo, date_patterns):
    """
    Find date mentions in a GitHub repository's text files.

    Args:
        repo (Repository): PyGithub Repository object.
        date_patterns (list): List of regular expression patterns for date matching.

    Returns:
        bool: True if date mentions are found, False otherwise.
        list: List of detected dates and line numbers.
    """
    try:
        detected_dates = []
        for file in repo.get_contents(""):
            if file.name.lower().endswith(".txt") and "en" in file.name.lower():
                try:
                    # Fetch the raw content of the text file
                    file_content_base64 = file.content

                    # Decode the base64 content
                    file_content = base64.b64decode(file_content_base64).decode(
                        "utf-8", errors="ignore"
                    )
                    for line_number, line in enumerate(
                        file_content.split("\n"), start=1
                    ):
                        for pattern in date_patterns:
                            matches = re.findall(pattern, line)
                            if matches:
                                detected_dates.append(
                                    f"Line {line_number}: Dates found - {matches}"
                                )

                    if detected_dates:
                        return True, detected_dates
                except UnicodeDecodeError:
                    print(f"Error decoding {file.name}: UnicodeDecodeError")
    except Exception as e:
        if "This repository is empty." in str(e):
            pass  # Ignore empty repository error
        else:
            print(f"Error accessing repository: {e}")
    return False, []


# date patterns are added here in this funciton
def get_date_patterns():
    """
    Provide regular expression patterns for common date formats.

    Returns:
        list of str: Regular expression patterns corresponding to common date formats.
    """
    ...

    patterns = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD, YYYY-DD-MM
        r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY, DD/MM/YYYY
        r"\d{4}/\d{2}/\d{2}",  # YYYY/DD/MM, YYYY/MM/DD
        r"\d{2}-\d{2}-\d{4}",  # DD-MM-YYYY, MM-DD-YYYY
        r"\d{4}",  # YYYY just year
        r"\d{1,2}(?:st|nd|rd|th)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s+\d{4}",  # 1st Nov, 2019
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(?:st|nd|rd|th),?\s+\d{4}",  # Nov 1st, 2019
        r"\d{1,2}(?:st|nd|rd|th)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}",  # 1st Nov 2019
        # Add more date formats as needed
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
        dict: Dictionary with repository names as keys and lists of detected dates and line numbers as values.
    """
    github = authenticate_github(token)
    org = github.get_organization(org_name)

    date_patterns = get_date_patterns()
    repos_with_dates = {}
    processed_repo = "processed_repo.txt"
    filewrite = "date_repo.txt"

    tm_repos = get_tm_repo_list(filepath, processed_repo)
    for tm_repo in tm_repos:
        repo = org.get_repo(tm_repo)
        date_detected, date_line_number = find_date_mentions_in_repo(
            repo, date_patterns
        )
        if date_detected:
            repos_with_dates[repo.name] = date_line_number
            write_to_file([tm_repo], filewrite)
            print(tm_repo, date_line_number)
        write_to_file([tm_repo], processed_repo)

    return repos_with_dates


if __name__ == "__main__":
    # Replace with your GitHub organization name and personal access token
    org_name = "MonlamAI"
    token = "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"
    filepath = "list.txt"
    date_file = "../../data/repo_dates.json"

    # Get repositories with date mentions
    repos_with_dates = filter_repositories_with_dates(org_name, token, filepath)

    # Print the list of repositories with date mentions
    print("Repositories containing date mentions:")
    for repo_name in repos_with_dates.keys():
        print(repo_name)
    with open(date_file, "w") as json_file:
        json.dump(repos_with_dates, json_file, indent=4)
