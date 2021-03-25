import os

DEFAULT_PATH = os.path.join('config.json')
DEFAULT_CONFIG_FILE = '''
{
  "Cantabular Credentials": {
    "username": "durham.project",
    "password": "extra.carrot.slowly",
    "key": null
  },
  "Cantabular Connection Information": {
    "address": "https://ftb-api-ext.ons.sensiblecode.io",
    "port": "8491"
  },
  "Nomis Credentials": {
    "username": "user",
    "password": "pass",
    "key": null
  },
  "Nomis Connection Information": {
    "address": "https://localhost",
    "port": "5001"
  },
  "Nomis Metadata Credentials": {
    "username": "user",
    "password": "pass",
    "key": null
  },
  "Nomis Metadata Connection Information": {
    "address": "https://localhost",
    "port": "5001"
  },
  "Geography Variables": [
    "OA",
    "LSOA",
    "MSOA",
    "LA",
    "MERGED_LA",
    "REGION",
    "COUNTRY",
    "Region",
    "Country"
  ]
}
'''
