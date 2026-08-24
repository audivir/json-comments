"""Compiled extension backing the `json_comments` package."""

def strip_json(data: str) -> str:
    """Strip comments and trailing commas from a JSON string.

    Strips C-style (`//`), block (`/* */`), and shell-style (`#`) comments,
    as well as trailing commas from a JSON string.
    Does not validate the JSON structure itself. If a block comment is unclosed (`/*`),
    the remainder of the string is treated as a comment and removed.

    Args:
        data: The raw JSON string which may contain comments or trailing commas.

    Returns:
        A cleaned JSON string ready for `json.loads()`.
    """
