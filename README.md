# json-comments

A Rust-backed JSON comment and trailing comma stripper for Python.

`json-comments` provides a single, simple utility to clean JSON-like strings before parsing them. It removes C-style (`//`), block (`/* */`), and shell-style (`#`) comments, as well as trailing commas from objects and arrays.

## Installation

```bash
pip install json-comments
```

## Usage

```python
import json
import json_comments

raw_data = """
{
    "foo": "bar", // c-style comment
    "baz": "qux", # shell-style comment
    "key": "value", /* block comment */
    "number": 123, // trailing comma
}
"""

# Strip comments and commas with `json_comments`
clean_json = json_comments.strip_json(raw_data)

# Parse with a JSON parser (e.g., `json` from the standard library)
data = json.loads(clean_json)
print(data)
# {'foo': 'bar', 'baz': 'qux', 'key': 'value', 'number': 123}
```

## Acknowledgements

This project is a Python wrapper around the [json-strip-comments](https://github.com/oxc-project/json-strip-comments) Rust crate (a fork of the original [json-comments-rs](https://github.com/tmccombs/json-comments-rs)).

Special thanks to:

- [tmccombs](https://github.com/tmccombs) for the original [json-comments-rs](https://github.com/tmccombs/json-comments-rs).
- The [oxc-project](https://github.com/oxc-project) for the [json-strip-comments](https://github.com/oxc-project/json-strip-comments) fork.

## License

MIT. See [LICENSE](LICENSE) for details including upstream copyright notices.
