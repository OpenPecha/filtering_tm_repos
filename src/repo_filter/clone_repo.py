import base64
import re

from repo_filter.list_repo import authenticate_github


def get_tm_repo_list(filepath1, filepath2):
    """
    Compare content of two files and return items unique to the first file.


    Args:
        filepath1 (str): Path to the first file.
        filepath2 (str): Path to the second file.

    Returns:
        list of str: Items found in the first file but not in the second.
    """
    ...

    with open(filepath1) as file1:
        # Read the lines and strip whitespace
        lines = file1.readlines()
        lines = [line.strip() for line in lines]
        # Convert the lines to integers (or other appropriate data types)
        my_list_1 = [str(line) for line in lines]
    with open(filepath2) as file2:
        # Read the lines and strip whitespace
        lines = file2.readlines()
        lines = [line.strip() for line in lines]
        # Convert the lines to integers (or other appropriate data types)
        my_list_2 = [str(line) for line in lines]
        result = [item for item in my_list_1 if item not in my_list_2]
    return result


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
                        if re.search(pattern, file_content):
                            return True
                except UnicodeDecodeError:
                    print(f"Error decoding {file.name}: UnicodeDecodeError")
    except Exception as e:
        if "This repository is empty." in str(e):
            pass  # Ignore empty repository error
        else:
            print(f"Error accessing repository: {e}")
    return False


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
    processed_repo = "processed_repo.txt"
    filewrite = "date_repo.txt"

    tm_repos = get_tm_repo_list(filepath, processed_repo)
    for tm_repo in tm_repos:
        repo = org.get_repo(tm_repo)

        if find_date_mentions_in_repo(repo, date_patterns):
            repos_with_dates.append(repo.name)
            write_to_file([tm_repo], filewrite)
            print(tm_repo)
        write_to_file([tm_repo], processed_repo)

    return repos_with_dates


if __name__ == "__main__":
    # Replace with your GitHub organization name and personal access token
    org_name = "MonlamAI"
    token = "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"
    filepath = "list.txt"

    # Get repositories with date mentions
    repos_with_dates = filter_repositories_with_dates(org_name, token, filepath)

    # Print the list of repositories with date mentions
    print("Repositories containing date mentions:")
    for repo_name in repos_with_dates:
        print(repo_name)
