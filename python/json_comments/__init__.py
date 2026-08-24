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

from __future__ import annotations

from json_comments._json_comments import strip_json

__all__ = ["strip_json"]
