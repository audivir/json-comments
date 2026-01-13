use pyo3::prelude::*;
use json_strip_comments::strip;

/// Strips C-style (//, /* */), Shell-style (#) comments, and trailing commas from a JSON string.
#[pyfunction]
fn strip_json(mut data: String) -> PyResult<String> {
    // strip() handles block comments, line comments, and trailing commas.
    // It modifies the string in-place for performance.
    strip(&mut data).map_err(|e| {
        pyo3::exceptions::PyValueError::new_err(format!("Failed to strip JSON: {}", e))
    })?;
    Ok(data)
}

/// The Python module definition.
#[pymodule]
fn json_comments(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(strip_json, m)?)?;
    Ok(())
}