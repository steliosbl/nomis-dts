from cantabular_client import CantabularClient
from variable import Variable
from variable_category import VariableCategory
from dataset_creation import DatasetCreation
from dataset_observations import DatasetObservations
from dummyApiConnector import DummyApiConnector
from configManager import ConfigManager


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

client = CantabularClient(cant.address, verify=True)

try:
    client.login(cant.username, cant.password)
except Exception as e:
    print("Error logging in: ", e)
    raise

print('Successfully logged into: ', client.base_request)

try:
    cb = client.codebook('Usual-Residents', get_categories=True)
except Exception as e:
    print('Error getting codebook: ', e)
    raise

try:
    table = client.query(cb, ['COUNTRY', 'HEALTH_T004A', 'SEX'])
except Exception as e:
    print('Error doing query: ', e)
    raise

print("______________")
print("")

print("Variable")
Variable = Variable(table)
var = Variable.variable_requests()
print(var)
print("______________")
print("")

print("VariableCategory")
VariableCategory = VariableCategory(table)
cat = VariableCategory.category_requests()
print(cat)
print("______________")
print("")

print("DatasetCreation")
DatasetCreation = DatasetCreation("syn01100", "TEST 1")
ds = DatasetCreation.dataset_request()
print(ds)
print("______________")
print("")

print("DatasetObservations")
DatasetObservations = DatasetObservations(table)
obs = DatasetObservations.observations_request()
print(obs)
print("______________")
print("")

###################################################################

creds = (nom.username, nom.password)
addr = nom.address

with DummyApiConnector(addr, creds) as connector:
    print(f"Connected to nomis mock server at {connector.client}.")
    print("")
    connector.dataset_exists("syn01100")
    print("")
    connector.create_dataset("syn01100", ds)
    print("")
    print(connector.get_dataset_dimensions("syn01100"))
    print("")
    # connector.assign_dimensions_to_dataset('1', dims)
    print("")
    connector.append_dataset_observations("syn01100", obs)
    print("")
    connector.overwrite_dataset_observations("syn01100", [obs, obs, obs])
    print("")
    connector.variable_exists("syn01100")
    print("")
    connector.create_variable("syn01100", var)
    print("")
    print(connector.get_variable_categories("syn01100"))
    print("")
    connector.create_variable_category('1',cat)
    print("")
    connector.update_variable_category("syn01100", "1", cat[0])
