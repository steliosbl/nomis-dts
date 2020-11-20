DEFAULT_PATH = './config.json'
DEFAULT_CONFIG_FILE = '''
{
  "Credentials": {
    "username": null,
    "password": null,
    "key": null
  },
  "Connection Information": {
    "cantabular_address": "127.0.0.1",
    "cantabular_port": "8491",
    "nomis_address": "127.0.0.1",
    "nomis_port": "1234" 
  },
  "Dataset Information": {
    "input_format": null,
    "output_format": "JSON",
    "data_type": "Data",
    "dataset_size": null
  }
}
'''  # idk the default port (or address) for the nomis api so just made it up for now
VALID_FORMATS = ["json", "csv"]  # Will be a list of acceptable input/output data formats for validation purposes
MAX_SIZE = 1000000  # arbitrary for now, might be pointless