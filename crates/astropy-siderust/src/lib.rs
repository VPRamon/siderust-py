use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use siderust::coordinates::centers::Geodetic;
use siderust::coordinates::frames::ECEF;
use siderust::event::horizontal::star_horizontal;
use siderust::qtty::{Degrees, Meters};
use siderust::time::constats::TT_MINUS_TAI;
use siderust::time::{try_jd_f64, ConversionError};

const BACKEND_NAME: &str = "siderust-py native extension";
const SIDERUST_VERSION: &str = "0.11.0";
const SIDERUST_SOURCE: &str = "crates.io";
const SIDERUST_FFI_SOURCE: &str =
    "Siderust/siderust.git:siderust-ffi, pinned when first FFI kernel lands";
const SIDERUST_FFI_ABI_VERSION: Option<u32> = None;
const SECONDS_PER_DAY: f64 = 86_400.0;

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

#[pyfunction]
fn tai_jd_to_tt_jd(jd1: Vec<f64>, jd2: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    if jd1.len() != jd2.len() {
        return Err(PyValueError::new_err(
            "jd1 and jd2 must contain the same number of values",
        ));
    }

    let offset_days = TT_MINUS_TAI.value() / SECONDS_PER_DAY;
    let out1 = jd1;
    let out2 = jd2.into_iter().map(|value| value + offset_days).collect();

    Ok((out1, out2))
}

fn validate_same_len(expected: usize, name: &str, actual: usize) -> PyResult<()> {
    if expected != actual {
        return Err(PyValueError::new_err(format!(
            "{name} must contain {expected} values, got {actual}"
        )));
    }
    Ok(())
}

fn validate_finite(name: &str, values: &[f64]) -> PyResult<()> {
    if values.iter().any(|value| !value.is_finite()) {
        return Err(PyValueError::new_err(format!(
            "{name} must contain only finite values"
        )));
    }
    Ok(())
}

fn map_time_error(error: ConversionError) -> PyErr {
    PyValueError::new_err(format!("invalid TT Julian date: {error:?}"))
}

#[pyfunction]
fn icrs_to_altaz_unit_spherical(
    ra_rad: Vec<f64>,
    dec_rad: Vec<f64>,
    obstime_tt_jd: Vec<f64>,
    longitude_rad: Vec<f64>,
    latitude_rad: Vec<f64>,
    height_m: Vec<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    let len = ra_rad.len();
    validate_same_len(len, "dec_rad", dec_rad.len())?;
    validate_same_len(len, "obstime_tt_jd", obstime_tt_jd.len())?;
    validate_same_len(len, "longitude_rad", longitude_rad.len())?;
    validate_same_len(len, "latitude_rad", latitude_rad.len())?;
    validate_same_len(len, "height_m", height_m.len())?;

    validate_finite("ra_rad", &ra_rad)?;
    validate_finite("dec_rad", &dec_rad)?;
    validate_finite("obstime_tt_jd", &obstime_tt_jd)?;
    validate_finite("longitude_rad", &longitude_rad)?;
    validate_finite("latitude_rad", &latitude_rad)?;
    validate_finite("height_m", &height_m)?;

    let mut az_rad = Vec::with_capacity(len);
    let mut alt_rad = Vec::with_capacity(len);

    for index in 0..len {
        let site = Geodetic::<ECEF>::new(
            Degrees::new(longitude_rad[index].to_degrees()),
            Degrees::new(latitude_rad[index].to_degrees()),
            Meters::new(height_m[index]),
        );
        let jd = try_jd_f64(obstime_tt_jd[index]).map_err(map_time_error)?;
        let horizontal = star_horizontal(
            Degrees::new(ra_rad[index].to_degrees()),
            Degrees::new(dec_rad[index].to_degrees()),
            &site,
            jd,
        );

        az_rad.push(horizontal.az().value().to_radians());
        alt_rad.push(horizontal.alt().value().to_radians());
    }

    Ok((az_rad, alt_rad))
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_function(wrap_pyfunction!(backend_name, m)?)?;
    m.add_function(wrap_pyfunction!(is_skeleton, m)?)?;
    m.add_function(wrap_pyfunction!(siderust_version, m)?)?;
    m.add_function(wrap_pyfunction!(dependency_info, m)?)?;
    m.add_function(wrap_pyfunction!(tai_jd_to_tt_jd, m)?)?;
    m.add_function(wrap_pyfunction!(icrs_to_altaz_unit_spherical, m)?)?;
    Ok(())
}
