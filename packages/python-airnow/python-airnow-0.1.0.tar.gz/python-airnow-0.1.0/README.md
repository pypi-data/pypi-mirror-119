[![CI](https://github.com/ronnie-llamado/python-airnow/actions/workflows/ci.yml/badge.svg)](https://github.com/ronnie-llamado/python-airnow/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ronnie-llamado/python-airnow/branch/main/graph/badge.svg?token=KJZNDU1Z6Q)](https://codecov.io/gh/ronnie-llamado/python-airnow)
[![Documentation Status](https://readthedocs.org/projects/python-airnow/badge/?version=latest)](https://python-airnow.readthedocs.io/en/latest/?badge=latest)
# python-airnow
A simple wrapper around [AirNow API](https://docs.airnowapi.org/).

## Install

```
pip install -U python-airnow
```

## Example

```python
import airnow

AIRNOW_API_KEY = '{INSERT_API_KEY}'
air = airnow.AirNow(AIRNOW_API_KEY)

obsrvtns = air.getObservationsByZipCode(20002)
print(obsrvtns)
# [
#     AirNowObservation(
#         DateTime=datetime.datetime(2021, 9, 7, 12, 0, tzinfo=tzoffset('EST', -18000)),
#         ReportingArea='Metropolitan Washington',
#         ParameterName='O3',
#         AQI=46
#     ),
#     AirNowObservation(
#         DateTime=datetime.datetime(2021, 9, 7, 12, 0, tzinfo=tzoffset('EST', -18000)),
#         ReportingArea='Metropolitan Washington',
#         ParameterName='PM2.5',
#         AQI=4
#     )
# ]

frcst = air.getForecastByLatLong(38.919, -77.013, date=datetime.datetime(2021,9,7))
print(frcst)
# [
#     AirNowForecast(
#       DateForecast=datetime.date(2021, 9, 7),
#       ReportingArea='Metropolitan Washington',
#       ParameterName='O3',
#       AQI=61
#     ),
#     AirNowForecast(
#       DateForecast=datetime.date(2021, 9, 7),
#       ReportingArea='Metropolitan Washington',
#       ParameterName='PM2.5',
#       AQI=38),
#     AirNowForecast(
#       DateForecast=datetime.date(2021, 9, 8),
#       ReportingArea='Metropolitan Washington',
#       ParameterName='O3',
#       AQI=50
#     ),
#     AirNowForecast(
#       DateForecast=datetime.date(2021, 9, 8),
#       ReportingArea='Metropolitan Washington',
#       ParameterName='PM2.5',
#       AQI=46
#     ),
#     AirNowForecast(
#       DateForecast=datetime.date(2021, 9, 9),
#       ReportingArea='Metropolitan Washington',
#       ParameterName='O3',
#       AQI=46
#     ),
#     AirNowForecast(
#       DateForecast=datetime.date(2021, 9, 9),
#       ReportingArea='Metropolitan Washington',
#       ParameterName='PM2.5',
#       AQI=33
#     )
# ]

```

## Links
- Documentation: https://python-airnow.readthedocs.io/
- PyPI Releases: https://pypi.org/project/python-airnow/
- Source Code: https://github.com/ronnie-llamado/python-airnow/
- Issue Tracker: https://github.com/ronnie-llamado/python-airnow/issues/
- AirNow API Documentation: https://docs.airnowapi.org
