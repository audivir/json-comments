use json_strip_comments::strip;
use pyo3::prelude::*;

/// Strip comments and trailing commas from a JSON string.
///
/// Strips C-style (`//`), block (`/* */`), and shell-style (`#`) comments,
/// as well as trailing commas from a JSON string.
/// Does not validate the JSON structure itself. If a block comment is unclosed (`/*`),
/// the remainder of the string is treated as a comment and removed.
///
/// Args:
///     data: The raw JSON string which may contain comments or trailing commas.
///
/// Returns:
///     A cleaned JSON string ready for `json.loads()`.
#[pyfunction]
fn strip_json(mut data: String) -> PyResult<String> {
    // strip() removes block comments, line comments, and trailing commas in-place.
    strip(&mut data).map_err(|e| {
        pyo3::exceptions::PyValueError::new_err(format!("Failed to strip JSON: {}", e))
    })?;
    Ok(data)
}

/// Rust-backed JSON comment and trailing comma stripper.
///
/// Provides a `strip_json` function that removes C-style (`//`), block (`/* */`),
/// and shell-style (`#`) comments, as well as trailing commas from JSON strings.
/// The result is a valid JSON string that can be parsed by json.loads() or similar JSON parsers.
///
/// Example:
///     >>> import json
///     >>> import json_comments
///     >>> json.loads(json_comments.strip_json("""\
///         {
///             "foo": "bar", // c-style comment
///             "baz": "qux", # shell-style comment
///             "key": "value", /* block comment */
///             "number": 123, // trailing comma
///         }
///     """))
///     {'foo': 'bar', 'baz': 'qux', 'key': 'value', 'number': 123}
#[pymodule]
fn json_comments(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(strip_json, m)?)?;
    Ok(())
}
