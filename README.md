# Predicted Runway In-Use MET Update

A standalone container that updates periodically the meteorological information of a set of airports.

## Configuration

The following environment variables can be used to configure the container:

- 'UPDATE_RATE': Defines the frequency at which the meteorological information will be updated. Given in minutes, defaults to 30.
- 'ICAO_CODES': Defines the airports for which meteorological updates will be retrieved. Given as a comma separated list of ICAO Codes. Defaults to 'EHAM,LFPO,LFBO'.
- 'AVWX_TOKEN': The AVWX API token used to retrieve the meteorological updates.