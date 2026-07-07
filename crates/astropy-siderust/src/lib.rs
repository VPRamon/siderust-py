use pyo3::prelude::*;

const BACKEND_NAME: &str = "siderust-py native extension skeleton";

#[pyfunction]
fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pyfunction]
fn backend_name() -> &'static str {
    BACKEND_NAME
}

#[pyfunction]
fn is_skeleton() -> bool {
    true
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_function(wrap_pyfunction!(backend_name, m)?)?;
    m.add_function(wrap_pyfunction!(is_skeleton, m)?)?;
    Ok(())
}
