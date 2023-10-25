def get_tm_repo_list(filepath1, filepath2):
    with open(filepath1) as file:
        # Read the lines and strip whitespace
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        # Convert the lines to integers (or other appropriate data types)
        my_list_1 = [str(line) for line in lines]
    with open(filepath2) as file:
        # Read the lines and strip whitespace
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        # Convert the lines to integers (or other appropriate data types)
        my_list_2 = [str(line) for line in lines]
        result = [item for item in my_list_1 if item not in my_list_2]
    return result


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


if __name__ == "__main__":
    filepath1 = "list.txt"
    filepath2 = "processed_repo.txt"
    tm_repos = get_tm_repo_list(filepath1, filepath2)
    print(tm_repos)
