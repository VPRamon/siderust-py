use pyo3::exceptions::{PyNotImplementedError, PyValueError};
use pyo3::prelude::*;
use siderust::time::constats::TT_MINUS_TAI;

const SECONDS_PER_DAY: f64 = 86_400.0;

const UTC_TAI_BLOCKER: &str = "time.utc_jd_to_tai_jd is blocked: siderust 0.11.0 does \
    not expose a public UTC/TAI leap-second conversion API for split Julian dates";

#[pyfunction]
pub(crate) fn tai_jd_to_tt_jd(jd1: Vec<f64>, jd2: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
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

#[pyfunction]
pub(crate) fn utc_jd_to_tai_jd(_jd1: Vec<f64>, _jd2: Vec<f64>) -> PyResult<Vec<f64>> {
    Err(PyNotImplementedError::new_err(UTC_TAI_BLOCKER))
}
