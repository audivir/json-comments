'''Rust-backed JSON comment and trailing comma stripper.

Provides a `strip_json` function that removes C-style (`//`), block (`/* */`),
and shell-style (`#`) comments, as well as trailing commas from JSON strings.
The result is a valid JSON string that can be parsed by json.loads() or similar JSON parsers.

Example:
    >>> import json
    >>> import json_comments
    >>> json.loads(json_comments.strip_json("""\
        {
            "foo": "bar", // c-style comment
            "baz": "qux", # shell-style comment
            "key": "value", /* block comment */
            "number": 123, // trailing comma
        }
    """))
    {'foo': 'bar', 'baz': 'qux', 'key': 'value', 'number': 123}

'''

def strip_json(data: str) -> str:
    """Strip comments and trailing commas from a JSON string.

    Strips C-style (`//`), block (`/* */`), and shell-style (`#`) comments,
    as well as trailing commas from a JSON string.
    Does not validate the JSON structure itself. If a block comment is unclosed (`/*`),
    the remainder of the string is treated as a comment and removed.

    Args:
        data: The raw JSON string which may contain comments or trailing commas.

    Returns:
        A cleaned JSON string ready for json.loads().

    """
