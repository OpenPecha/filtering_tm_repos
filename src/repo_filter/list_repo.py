from github import Github


def authenticate_github(token):
    """
    Authenticate to GitHub using a personal access token.

    Args:
        token (str): Personal access token for GitHub.

    Returns:
        Github: A PyGithub instance authenticated with the provided token.
    """
    # Create a PyGithub instance with the personal access token
    g = Github(token)
    return g


def list_repos_starting_with_tm(token, org_name):
    """
    List all repositories in the specified organization that start with 'tm'.

    Parameters:
    token (str): The personal access token for GitHub authentication.
    org_name (str): The name of the organization on GitHub.

    Returns:
    list of str: A list of repository names.
    """

    # Initialize a GitHub instance using an access token
    g = authenticate_github(token)

    try:
        # Get the organization
        org = g.get_organization(org_name)

        # Get list of repos from the organization
        all_repos = org.get_repos()

        # Filter repositories that start with 'tm'
        tm_repos = [
            repo.name for repo in all_repos if repo.name.lower().startswith("tm")
        ]

        return tm_repos

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def write_file(data, filename):
    with open(filename, "w") as file:
        for line in data:
            file.write(line + "\n")  # The '\n' is a newline character


def get_tm_repo_list(filepath):
    with open(filepath) as file:
        # Read the lines and strip whitespace
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        # Convert the lines to integers (or other appropriate data types)
        my_list = [str(line) for line in lines]
    return my_list


# Usage
if __name__ == "__main__":
    personal_access_token = (
        "Personal Token"  # replace with your GitHub personal access token
    )
    organization_name = "MonlamAI"  # or 'monlamai' if that's the actual name
    filename = "list.txt"
    repositories = list_repos_starting_with_tm(personal_access_token, organization_name)

    if repositories is not None:
        cnt = 0
        write_file(repositories, filename)
        print('Repositories starting with "tm":')
        for repo_name in repositories:
            cnt = cnt + 1
            print(cnt, repo_name)
