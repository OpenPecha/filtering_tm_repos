import re


def get_tm_repo_list(filepath):
    with open(filepath) as file:
        # Read the lines and strip whitespace
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        # Convert the lines to integers (or other appropriate data types)
        my_list = [str(line) for line in lines]
    return my_list


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
    filepath = "list.txt"
    tm_repos = get_tm_repo_list(filepath)
    # print(tm_repos)
    file_content = "in year 2000"
    pat = get_date_patterns()
    for pattern in pat:
        dates_found = re.findall(pattern, file_content)
        if dates_found:
            print(True)
        else:
            print(False)
