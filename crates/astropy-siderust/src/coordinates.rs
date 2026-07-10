use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use siderust::coordinates::centers::Geodetic;
use siderust::coordinates::frames::ECEF;
use siderust::event::horizontal::star_horizontal;
use siderust::qtty::{Degrees, Meters};
use siderust::time::{try_jd_f64, ConversionError};

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
pub(crate) fn icrs_to_altaz_unit_spherical(
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
