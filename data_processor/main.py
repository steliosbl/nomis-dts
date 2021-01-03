"""Script performs a JSON-stat query."""
import csv
from variable import Variable
from variable_category import VariableCategory 
from dataset_observations import DatasetObservations
from dataset_creation import DatasetCreation
from cantabular_connector import CantabularConnector
import json


BASE_URL = 'https://ftb-api-ext.ons.sensiblecode.io'
DATASET = 'Usual-Residents'
VARIABLES = ['COUNTRY', 'HEALTH', 'SEX']
# A query with the following categories will have some areas that fail
# disclosure control rules checks.
# VARIABLES = ['LSOA', 'AGE_T005B', 'CARER']
# A query with the following variables will result in a MAX_CELLS error
# as the output table would have more cells than permitted.
# VARIABLES = ['OA', 'AGE', 'CARER']

# Read credentials from a text file. The file should have the format:
# username,password
with open('creds.txt') as password_file:
    READER = csv.reader(password_file)
    CREDENTIALS = next(READER)

cantabularConnector = CantabularConnector('https://ftb-api-ext.ons.sensiblecode.io', CREDENTIALS)
table = cantabularConnector.query(DATASET, VARIABLES)

variable = Variable(table)
variables = variable.variable_requests()
print(json.dumps(variables, indent=3))

#variableCategory = VariableCategory(PYJSTAT_DATAFRAME)
#categories = variableCategory.category_requests()
#print(categories)

datsetObservations = DatasetObservations(table)
observations = datsetObservations.observations_request()
print(json.dumps(observations, indent=3))

#print(PYJSTAT_DATAFRAME["value"])




#print(PYJSTAT_DATAFRAME[0])