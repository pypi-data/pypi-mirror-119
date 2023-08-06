# matchms-plotly

Plot [Matchms](https://matchms.readthedocs.io) spectra with [Plotly](https://plotly.com/python/).

This package is under developement for the [MetWork](www.metwork.science) project.

## Install

```bash
pip install matchms-plotly
```

## Usage

```python
from matchms_plotly import plot_spectrum, plot_spectra

# Plot a single spectrum.
plot_spectrum(spectrum)

# Plot two spectrums in the "up and down" fashion.
plot_spectra(spectrum_up, spectrum_down)
```
