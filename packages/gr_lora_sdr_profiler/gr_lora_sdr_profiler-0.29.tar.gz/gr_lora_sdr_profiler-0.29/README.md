# gr-lora_sdr-profiler

> Profile different flowgraph configurations of [gr-lora_sdr](https://github.com/martynvdijke/gr-lora_sdr)

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]

## Summary
This is a python cli package to be able to load a config yml file and change values to the flowgraph and run the flowgraph.
## Installation

```sh
$ pip install gr_lora_sdr_profiler
```
## Documentation

```python
[-h] 
[--version] 
[-m {multi_stream,frame_detector-sim,frame_detector-usrp,cran-sim,cran-usrp}]
[-s {pandas,wandb,both}] 
[-n NAME] 
[-p FILE] 
[-o OUTPUT] 
[-t TIMEOUT] 
[--no_remove_temp]
[--sequential_spreading_factor]
[-v] 
[-vv] 
FILE [FILE ...]
```
## Usage

### config
the config files are parsed on launch of the script and are fed into the flowgraph script.

### cli
Run flowgraph 
```python
$ python -m profiler --m frame_detector -s pandas example_config.yml 
```
Plot all values by using 
```python
$ python -m profiler --m frame_detector -p results/out.csv example_config.yml 
```

## Development setup

```sh
$ python3 -m venv env
$ . env/bin/activate
$ make deps
$ tox
```
## [Changelog](CHANGELOG.md)

## License

[MIT](https://choosealicense.com/licenses/mit/)

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/gr_lora_sdr_profiler
[pypi-url]: https://pypi.org/project/gr_lora_sdr_profiler/
[build-image]: https://github.com/martynvdijke/gr-lora_sdr-profiler/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/martynvdijke/gr-lora_sdr-profiler/actions/workflows/build.yml