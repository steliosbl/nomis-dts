from cantabular_client import LOGGER
from cantabular_client import CantabularClient
from variable import Variable
from variable_category import VariableCategory
from dataset_creation import DatasetCreation
from dataset_observations import DatasetObservations
import logging
import csv
import json
import numpy as np

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logging.getLogger().addHandler(handler)
LOGGER.setLevel(logging.INFO)

# Create an instance of CantabularClient and pass in
# the URL of the Cantabular server. The verify parameter
# can be set to False to disable TLS certificate verification
# or to the name (including path) of a CA bundle file.
client = CantabularClient('https://ftb.ons.sensiblecode.io', verify=True)

# Store your credentials in a text file with
# a single line of the format:
# username,password
credentials = dict()
try:
    with open('creds.txt') as password_file:
        reader = csv.reader(password_file)
        credentials = next(reader)
except Exception as e:
        print('Error reading credentials file: ', e)
        raise

if len(credentials) != 2:
    print('Invalid credentials fle')
    raise Exception

# Log in to gain access to the API. A requests.Session
# instance is used to keep track of authentication tokens.
try:
    client.login(credentials[0], credentials[1])
except Exception as e:
    print("Error logging in: ", e)
    raise
    
print('Successfully logged into: ', client.base_request)


# Download the codebook for the Usual-Residents dataset.
# With get_categories set to False, detailed category
# information is omitted, substantially reducing the download
# size.
try:
    cb = client.codebook('Usual-Residents', get_categories=True)
except Exception as e:
    print('Error getting codebook: ', e)
    raise  

# Perform a query using the codebook and three variables.
# As part of the query method a call will be made to the API
# to get detailed category information for the variables. This
# information is stored in the codebook and reused for future
# queries using any of the variables.https://tljh.sensiblecode.io/user/scc/kernelspecs/python3/logo-64x64.png
try:
    table = client.query(cb, ['COUNTRY', 'HEALTH_T004A', 'SEX'])
except Exception as e:
    print('Error doing query: ', e)
    raise

Variable = Variable(table)
print(VariableRequest.variable_requests())

VariableCategory = VariableCategory(table)
print(VariableCategoryRequest.category_requests())

DatasetCreation = DatasetCreation("syn1", "TEST 1")
print(DatasetCreation.dataset_request())

DatasetObservations = DatasetObservations(table)
print(DatasetObservations.observations_request())
    

# The returned data can be printed as a string.
# The counts are a flat tuple of integers.
