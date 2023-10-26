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
