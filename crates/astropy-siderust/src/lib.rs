mod coordinates;
mod time;

use pyo3::prelude::*;
use pyo3::types::PyDict;

const BACKEND_NAME: &str = "siderust-py native extension";
const SIDERUST_VERSION: &str = "0.11.0";
const SIDERUST_SOURCE: &str = "crates.io";
const SIDERUST_FFI_SOURCE: &str =
    "Siderust/siderust.git:siderust-ffi, pinned when first FFI kernel lands";
const SIDERUST_FFI_ABI_VERSION: Option<u32> = None;

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
    false
}

#[pyfunction]
fn siderust_version() -> &'static str {
    SIDERUST_VERSION
}

#[pyfunction]
fn dependency_info(py: Python<'_>) -> PyResult<Bound<'_, PyDict>> {
    let info = PyDict::new(py);
    info.set_item("siderust_version", SIDERUST_VERSION)?;
    info.set_item("siderust_source", SIDERUST_SOURCE)?;
    info.set_item("siderust_ffi_source", SIDERUST_FFI_SOURCE)?;
    info.set_item("siderust_ffi_abi_version", SIDERUST_FFI_ABI_VERSION)?;
    Ok(info)
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_function(wrap_pyfunction!(backend_name, m)?)?;
    m.add_function(wrap_pyfunction!(is_skeleton, m)?)?;
    m.add_function(wrap_pyfunction!(siderust_version, m)?)?;
    m.add_function(wrap_pyfunction!(dependency_info, m)?)?;
    m.add_function(wrap_pyfunction!(time::tai_jd_to_tt_jd, m)?)?;
    m.add_function(wrap_pyfunction!(time::utc_jd_to_tai_jd, m)?)?;
    m.add_function(wrap_pyfunction!(
        coordinates::icrs_to_altaz_unit_spherical,
        m
    )?)?;
    Ok(())
}
