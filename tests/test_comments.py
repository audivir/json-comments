import json

import json_comments


def test_line_comments() -> None:
    """Tests C-style and Shell-style line comments."""
    dirty = """
    {
        // This is a C-style comment
        "key": "value", # This is a shell-style comment
        "number": 123 // another one
    }
    """
    clean = json_comments.strip_json(dirty)
    data = json.loads(clean)
    assert data == {"key": "value", "number": 123}


def test_block_comments() -> None:
    """Tests multi-line block comments."""
    dirty = """
    {
        /* Multi-line
           block comment */
        "key": /* inline comment */ "value"
    }
    """
    clean = json_comments.strip_json(dirty)
    data = json.loads(clean)
    assert data == {"key": "value"}


def test_non_trailing_comments() -> None:
    """Tests non-trailing block comments."""
    dirty = """
    {
        "key": /* before value */ "value",
        "null" /* after key */ : null,
        /* before key */ "number": 123,
    }
    """
    clean = json_comments.strip_json(dirty)
    data = json.loads(clean)
    assert data == {"key": "value", "null": None, "number": 123}


def test_invalid_json() -> None:
    """Tests handling of invalid JSON."""
    dirty = '{"key": "value", /* comment */'
    clean = json_comments.strip_json(dirty)
    # mind the whitespace instead of the comment
    assert clean == '{"key": "value",              '


def test_incomplete_comments() -> None:
    """Tests handling of incomplete comments."""
    dirty = '{"key": "value", /* comment'
    clean = json_comments.strip_json(dirty)
    # mind the whitespace instead of the comment
    assert clean == '{"key": "value",           '


def test_trailing_commas() -> None:
    """Tests removal of trailing commas in objects and arrays."""
    dirty = """
    {
        "array": [
            1,
            2,
            3,
        ],
        "object": {
            "a": 1,
        },
    }
    """
    clean = json_comments.strip_json(dirty)
    data = json.loads(clean)
    assert data == {"array": [1, 2, 3], "object": {"a": 1}}


def test_comments_in_strings() -> None:
    """Ensures that symbols inside strings are NOT stripped."""
    dirty = '{ "url": "https://example.com", "msg": "/* not a comment */" }'
    clean = json_comments.strip_json(dirty)
    data = json.loads(clean)
    assert data == {"url": "https://example.com", "msg": "/* not a comment */"}


def test_nested_structures() -> None:
    """Test case with a nested object, comments in all styles, and trailing commas."""
    dirty = """
    {
        "a": [ { "b": 1, }, # comment
        ], // comment
        /* block */
        "c": 2,
    }
    """
    clean = json_comments.strip_json(dirty)
    data = json.loads(clean)
    assert data == {"a": [{"b": 1}], "c": 2}
