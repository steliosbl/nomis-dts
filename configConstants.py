DEFAULT_PATH = './config.json'
DEFAULT_CONFIG_FILE = '''
{
  "Cantabular Credentials": {
    "username": null,
    "password": null,
    "key": null
  },
  "Cantabular Connection Information": {
    "api": "cantabular",
    "address": "localhost",
    "port": "8491"
  },
  "Nomis Credentials": {
    "username": null,
    "password": null,
    "key": null
  },
  "Nomis Connection Information": {
    "api": "nomis",
    "address": "https://www.nomisweb.co.uk/api/v2",
    "port": "1234"
  },
  "Dataset Information": {
    "input_format": null,
    "output_format": "JSON",
    "data_type": "Data",
    "dataset_size": null
  }
}
'''
VALID_FORMATS = ["json", "csv"]  # Will be a list of acceptable input/output data formats for validation purposes
MAX_SIZE = 1000000  # arbitrary for now, might be pointless
