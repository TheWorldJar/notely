from src import fileactions


def test_get_extension():
    res = fileactions.get_extension("src/prompt.txt")
    assert res == ".txt"
    res = fileactions.get_extension("src/prompts/prompt.txt")
    assert res == ".txt"
    res = fileactions.get_extension("src/prompt.txt.md")
    assert res == ".md"


def test_get_file_hash():
    hash1 = fileactions.get_file_hash("./src/tests/test.txt")
    hash2 = fileactions.get_file_hash("./src/tests/test2.txt")
    assert hash1 == hash2


def test_get_file_content():
    content = fileactions.read_file("./src/tests/test.txt")
    assert (
        content
        == "This is a test file to validate file hashing! This file should have the same hash as the other test file!"
    )
