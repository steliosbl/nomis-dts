"""Script performs a JSON-stat query."""
from cantabular_connector import CantabularConnector
from nomis_api_connector import NomisApiConnector
from config_manager import ConfigManager
from api_connection_info import ApiConnectionInfo
from args_manager import ArgsManager
from read_from_file import ReadFromFile
from dataset_transformations import DatasetTransformations
from logger import Logger
import json


def new_dataset(nomis_info: ApiConnectionInfo,
                cantabular_info: ApiConnectionInfo,
                args: ArgsManager) -> None:
    nomis_url = nomis_info.get_client()
    nomis_creds = nomis_info.get_credentials()
    cantabular_url = cantabular_info.address
    cantabular_creds = cantabular_info.get_credentials()
    dataset_id, dataset_title, query_variables = args.dataset_id, args.dataset_title, args.query_variables
    query_dataset, y_flag, filename = args.query_dataset, args.y_flag, args.filename

    # Query cantabular using given variables
    if filename is not None:
        read_from_file = ReadFromFile("query_file_example.json")
        table = read_from_file.read()
    else:
        cantabular_connector = CantabularConnector(cantabular_url, cantabular_creds)
        table = cantabular_connector.query(query_dataset, query_variables)

    ds_transformations = DatasetTransformations(table)

    # Create instance of nomis connector
    nomis_connector = NomisApiConnector(nomis_url, nomis_creds)

    # Check to see if a dataset already exists with this id
    dataset_exists_code = nomis_connector.dataset_exists(dataset_id)

    if not dataset_exists_code:
        # Create a new dataset with given id

        print("-----DATASET CREATION-----")
        dataset_request_body = ds_transformations.dataset_creation(dataset_id, dataset_title)
        nomis_connector.create_dataset(dataset_id, dataset_request_body)

        # Create the variable creation request bodies
        variable_request_body = ds_transformations.variable_creation()

        # Create the category request bodies
        category_request_body = ds_transformations.category_creation()

        # Check to see variables already exist for the given dimensions
        print("\n-----VARIABLE CREATION-----")
        for variable in query_variables:

            variable_exists_code = nomis_connector.variable_exists(variable)

            # IF the variable does NOT exist then create it
            if not variable_exists_code:  # mock server always returns True so this is for testing purposes.
                for request in variable_request_body:
                    if request["name"] == variable:
                        nomis_connector.create_variable(variable, request)
                    else:
                        continue

                # Create the categories for this new variable as well.
                requests = []
                for category in table["dimension"][variable]["category"]["index"]:
                    for request in category_request_body:
                        if category == request["code"] and table["dimension"][variable] \
                                ["category"]["label"][category] == request["title"]:
                            requests.append(request)
                        else:
                            continue
                nomis_connector.create_variable_category(variable, requests)

            else:
                continue
        print("\n-----ASSIGNING DIMENSIONS-----")
        # Assign dimensions to dataset
        assign_dimensions_requests = ds_transformations.assign_dimensions()
        nomis_connector.assign_dimensions_to_dataset(dataset_id, assign_dimensions_requests)

        print("\n-----APPENDING OBSERVATIONS-----")
        # Append observations into dataset
        observations_requests = ds_transformations.observations(dataset_id)
        nomis_connector.overwrite_dataset_observations(dataset_id, observations_requests)

        print(f"\nSUCCESS: A dataset with the ID {dataset_id} has been CREATED successfully.")

    else:
        raise Exception("A dataset with this ID already exists.")


def update_dataset(nomis_info: ApiConnectionInfo,
                   cantabular_info: ApiConnectionInfo,
                   args: ArgsManager) -> None:
    nomis_url = nomis_info.get_client()
    nomis_creds = nomis_info.get_credentials()
    cantabular_url = cantabular_info.address
    cantabular_creds = cantabular_info.get_credentials()
    dataset_id, dataset_title, query_variables = args.dataset_id, args.dataset_title, args.query_variables
    query_dataset, y_flag, filename = args.query_dataset, args.y_flag, args.filename

    # Query cantabular using given variables
    if filename is not None:
        read_from_file = ReadFromFile("cantabular_query_example.json")
        table = read_from_file.read()
    else:
        cantabular_connector = CantabularConnector(cantabular_url, cantabular_creds)
        table = cantabular_connector.query(query_dataset, query_variables)

    ds_transformations = DatasetTransformations(table)

    # Create instance of nomis connector
    nomis_connector = NomisApiConnector(nomis_url, nomis_creds)

    # Check to see if a dataset already exists with this id
    dataset_exists_code = nomis_connector.dataset_exists(dataset_id)

    if dataset_exists_code:

        print("\n-----RETRIEVING DIMENSIONS-----")
        assigned_variables_json = nomis_connector.get_dataset_dimensions(dataset_id)
        assigned_variables = []
        non_assigned_variables = []

        # Get all of the currently assigned variables in a list by variable name
        for variable in assigned_variables:
            assigned_variables.append(variable["variable"]["name"])

        # Check to see if any of the variables in the observation request
        for variable in query_variables:
            if variable not in assigned_variables:
                non_assigned_variables.append(variable)

        # Create any new variables and assign all non assigned variables to the dataset
        if len(non_assigned_variables) > 0:

            # Create the variable creation request bodies
            variable_request_body = ds_transformations.variable_creation()

            # Create the category request bodies
            category_request_body = ds_transformations.category_creation()

            # Check to see variables already exist for the given dimensions
            print("\n-----VARIABLE CREATION-----")
            for variable in query_variables:
                variable_exists_code = nomis_connector.variable_exists(variable)

                # IF the variable does NOT exist then create it
                if not variable_exists_code:  # mock server always returns True so this is for testing purposes.
                    for request in variable_request_body:
                        if request["name"] == variable:
                            nomis_connector.create_variable(variable, request)
                        else:
                            continue

                    # Create the categories for this new variable as well.
                    requests = []
                    for category in table["dimension"][variable]["category"]["index"]:
                        for request in category_request_body:
                            if category == request["code"] and table["dimension"][variable]["category"]\
                                    ["label"][category] == request["title"]:
                                requests.append(request)
                            else:
                                continue
                    nomis_connector.create_variable_category(variable, requests)
                else:
                    continue

            # Assign dimensions to dataset
            print("\n-----OVERWRITING DIMENSIONS-----")
            nomis_connector.delete_dimensions(dataset_id)
            assign_dimensions_requests = ds_transformations.assign_dimensions()
            nomis_connector.assign_dimensions_to_dataset(dataset_id, assign_dimensions_requests)

        # Append observations into dataset
        print("\n-----OVERWRITING OBSERVATIONS-----")
        observations_request = ds_transformations.observations(dataset_id)
        nomis_connector.overwrite_dataset_observations(dataset_id, observations_request)

        print(f"\nSUCCESS: A dataset with the ID {dataset_id} has been UPDATED successfully.")

    else:
        raise Exception("A dataset with this ID does NOT exist.")


##############################


args = ArgsManager()
logs = Logger(verbose=args.v_flag, log_file=args.log_file)


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
print(nom.port + "\n")
#################################################################

########## EXAMPLES ##########

nomis_creds = (nom.username, nom.password)
nomis_addr = nom.get_client()

cantabular_addr = cant.address
cantabular_creds = (cant.username, cant.password)

nomis_connector = NomisApiConnector(nomis_addr, nomis_creds)

is_update = "y"

if nomis_connector.dataset_exists(args.dataset_id):

    if not args.y_flag:
        is_update = str(input(
            "--- A DATASET WITH THE ID " + args.dataset_id + " ALREADY EXISTS ---\n*** DO YOU WANT TO OVERWRITE/UPDATE y/n ***\n"))

    if is_update == "y":
        update_dataset(nom, cant, args)

    elif is_update == "n":
        print("*** DATASET HAS NOT BEEN UPDATED ***")

    else:
        raise Exception("'" + is_update + "' is not a valid option. Please try again!")
else:
    new_dataset(nom, cant, args)
