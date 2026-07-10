# astropy.convolution

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.convolution` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `convolve`, `convolve_fft`, `interpolate_replace_nans`
- Kernel classes: `Gaussian1DKernel`, `Box1DKernel`, `Model1DKernel`, etc.
- `convolve_models` — model convolution

## Current backend

Cython extension `astropy/convolution/_convolve.pyx` for discrete convolution;
NumPy/SciPy for FFT paths.

## Siderust coverage today

None.

## Gap list

Image/array convolution, kernel generation, and boundary handling.

## Proposed kernel names

None planned (outside initial acceleration scope per README non-goals).

## Blockers

General signal-processing kernels are not part of Siderust's astronomy scope.

## Fallback behavior

All convolution uses Cython/NumPy/SciPy paths unchanged.
