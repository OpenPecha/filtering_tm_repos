from repo_filter.clone_repo import get_tm_repo_list
from repo_filter.example import add_one


def test_get_tm_repo_list():
    filepath1 = "list1.txt"
    filepath2 = "list2.txt"
    assert get_tm_repo_list(filepath1, filepath2) == [4, 5]


def test_add_one():
    assert add_one(1) == 2
