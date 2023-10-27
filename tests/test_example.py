from repo_filter.example import add_one
from repo_filter.testing import get_tm_repo_list


def test_get_tm_repo_list():
    filepath1 = "./data/list1.txt"
    filepath2 = "./data/list2.txt"
    assert get_tm_repo_list(filepath1, filepath2) == ["4", "5"]


def test_add_one():
    assert add_one(1) == 2
