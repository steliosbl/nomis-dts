"""Script performs a JSON-stat query."""
from variable import Variable
from variable_category import VariableCategory 
from dataset_observations import DatasetObservations
from dataset_creation import DatasetCreation
from assign_dimensions import AssignDimensions
from cantabular_connector import CantabularConnector
from dummyApiConnector import DummyApiConnector
from configManager import ConfigManager
import json

def new_dataset(nomis_url, nomis_creds, cantabular_url, cantabular_creds, dataset_id, dataset_title, query_variables, query_dataset):
	#Query cantabular using given variables
	cantabular_connector = CantabularConnector(cantabular_url, cantabular_creds)
	table = cantabular_connector.query(query_dataset, query_variables)

	#Create instance of nomis connector
	nomis_connector = DummyApiConnector(nomis_url, nomis_creds)

	#Check to see if a dataset already exists with this id
	dataset_exists_code = nomis_connector.dataset_exists(dataset_id)

	if dataset_exists_code == True:
		#Create a new dataset with given id
		dataset_creation = DatasetCreation(dataset_id, dataset_title)
		dataset_request_body = dataset_creation.dataset_request()
		nomis_connector.create_dataset(dataset_id, dataset_request_body)

		#Create the variable creation request bodies
		variable_creation = Variable(table)
		variable_request_body = variable_creation.variable_requests()

		#Create the category request bodies
		category_creation = VariableCategory(table)
		category_request_body = category_creation.category_requests()

		#Check to see variables already exist for the given dimensions
		for variable in query_variables:
			variable_exists_code = nomis_connector.variable_exists(variable)

			#IF the variable does NOT exist then create it
			if variable_exists_code == True: #mock server always returns True so this is for testing purposes.
				for request in variable_request_body:
					if request["name"] == variable:
						nomis_connector.create_variable(variable, request)
					else:
						continue

				
				#Create the categories for this new variable as well.
				requests = []
				for category in table["dimension"][variable]["category"]["index"]:
					for request in category_request_body:
						if category == request["code"] and table["dimension"][variable]["category"]["label"][category] == request["title"]:
							requests.append(request)
						else:
							continue
				nomis_connector.create_variable_category(variable, requests)
			else:
				continue

		#Assign dimensions to dataset
		assign_dimensions = AssignDimensions(table)
		assign_dimensions_requests = assign_dimensions.assign_dimensions_requests()

		nomis_connector.assign_dimensions_to_dataset(dataset_id, assign_dimensions_requests)

		#Append observations into dataset
		observations = DatasetObservations(table)
		observations_requests = observations.observations_request()

		nomis_connector.append_dataset_observations(dataset_id, observations_requests)

		print("SUCCESS")
		print(table)

##############################
c = ConfigManager()

print("")
print("Configuration")
config = c.decode_into_configuration()
print(config.validate())

print("")
print("Cantabular Credentials")
cant_creds = c.decode_into_cantabular_credentials()
print(cant_creds.validate())

print("")
print("Cantabular Connecton Information")
cant_conn = c.decode_into_cantabular_connection_info()
print(cant_conn.validate())

print("")
print("Nomis Credentials")
nom_creds = c.decode_into_nomis_credentials()
print(nom_creds.validate())

print("")
print("Nomis Connecton Information")
nom_conn = c.decode_into_nomis_connection_info()
print(nom_conn.validate())

print("")
print("Cantabular Complete API Connecton Information")
cant = c.create_api_connection_info(cant_creds, cant_conn)
print(cant.port)

print("")
print("Nomis Complete API Connecton Information")
nom = c.create_api_connection_info(nom_creds, nom_conn)
print(nom.port)
#################################################################



nomis_creds = (nom.username, nom.password)
nomis_addr = nom.address

cantabular_addr = cant.address
cantabular_creds = [cant.username, cant.password]

new_dataset(nomis_addr, nomis_creds, cantabular_addr, cantabular_creds, "syn123", "TEST 1", ['COUNTRY', 'SEX', "HEALTH"], 'Usual-Residents')











############# Example ##############
# cantabularConnector = CantabularConnector('https://ftb-api-ext.ons.sensiblecode.io', cantabular_creds)
# table = cantabularConnector.query("Usual-Residents", ["COUNTRY", "SEX"])

# print(table)

# variable = Variable(table)
# variables = variable.variable_requests()
# print(json.dumps(variables, indent=3))

# variableCategory = VariableCategory(table)
# categories = variableCategory.category_requests()
# print(json.dumps(categories, indent=3))

# datsetObservations = DatasetObservations(table)
# observations = datsetObservations.observations_request()
# print(json.dumps(observations, indent=3))

# print(PYJSTAT_DATAFRAME["value"])




#print(PYJSTAT_DATAFRAME[0])