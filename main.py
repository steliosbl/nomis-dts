"""Script performs a JSON-stat query."""
from cantabular_api_connector import CantabularApiConnector
from nomis_api_connector import NomisApiConnector
from config_manager import ConfigManager
from configuration import Configuration
from args_manager import ArgsManager, Arguments
from dataset_file_reader import DatasetFileReader
from dataset_transformations import DatasetTransformations
import logging
import sys


# Initialise logging

logger = logging.getLogger('DTS-Logger')
logger.propagate = False
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s; in %(filename)s] %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
file_handler = logging.FileHandler("system.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Collect arguments

with ArgsManager() as a:
    arguments = a.get_args()

if arguments.verbose:
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)

if arguments.log_file is not None:  # change s.t. replaces not appends
    new_file_handler = logging.FileHandler(arguments.log_file)
    new_file_handler.setFormatter(formatter)
    logger.addHandler(new_file_handler)


# Establish configuration

with ConfigManager(arguments) as c:
    config = c.decode_configuration()


def new_dataset(config: Configuration,
                args: Arguments
                ) -> None:

    nomis_url = config.get_client('nomis')
    nomis_creds = config.get_credentials('nomis')
    cantabular_url = config.cantabular_api_info.address
    cantabular_creds = config.get_credentials('cantabular')
    dataset_id, dataset_title, query_variables = args.dataset_id, args.dataset_title, args.query_variables
    query_dataset, y_flag, filename = args.query_dataset, args.suppress_prompts, args.filename

    # Query cantabular using given variables
    if filename is not None:
        read_from_file = DatasetFileReader(args.filename)
        table = read_from_file.query()
    else:
        with CantabularApiConnector(query_dataset, query_variables, cantabular_creds, cantabular_url) as cc:
            table = cc.query()

    ds_transformations = DatasetTransformations(table)

    # Create instance of nomis connector
    nomis_connector = NomisApiConnector(nomis_creds, nomis_url)

    # Check to see if a dataset already exists with this id
    dataset_exists_code = nomis_connector.get_dataset(dataset_id, return_bool=True)

    if not dataset_exists_code:
        # Create a new dataset with given id

        logger.info("-----DATASET CREATION-----")
        dataset_request_body = ds_transformations.dataset_creation(dataset_id, dataset_title)
        nomis_connector.create_dataset(dataset_id, dataset_request_body)

        # Create the variable creation request bodies
        variable_request_body = ds_transformations.variable_creation()

        # Create the category request bodies
        category_request_body = ds_transformations.category_creation()

        # Check to see variables already exist for the given dimensions
        logger.info("\n-----VARIABLE CREATION-----")
        for variable in query_variables:

            variable_exists_code = nomis_connector.get_variable(variable, return_bool=True)

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
        logger.info("\n-----ASSIGNING DIMENSIONS-----")
        # Assign dimensions to dataset
        assign_dimensions_requests = ds_transformations.assign_dimensions()
        nomis_connector.assign_dimensions_to_dataset(dataset_id, assign_dimensions_requests)

        logger.info("\n-----APPENDING OBSERVATIONS-----")
        # Append observations into dataset
        observations_requests = ds_transformations.observations(dataset_id)
        nomis_connector.overwrite_dataset_observations(dataset_id, observations_requests)

        logger.info(f"\nSUCCESS: A dataset with the ID {dataset_id} has been CREATED successfully.")

    else:
        raise Exception("A dataset with this ID already exists.")


def update_dataset(config: Configuration,
                   args: Arguments) -> None:
    nomis_url = config.get_client('nomis')
    nomis_creds = config.get_credentials('nomis')
    cantabular_url = config.cantabular_api_info.address
    cantabular_creds = config.get_credentials('cantabular')
    dataset_id, dataset_title, query_variables = args.dataset_id, args.dataset_title, args.query_variables
    query_dataset, y_flag, filename = args.query_dataset, args.suppress_prompts, args.filename

    # Query cantabular using given variables
    if filename is not None:
        read_from_file = DatasetFileReader("cantabular_query_example.json")
        table = read_from_file.query()
    else:
        with CantabularApiConnector(query_dataset, query_variables, cantabular_creds, cantabular_url) as cc:
            table = cc.query()

    ds_transformations = DatasetTransformations(table)

    # Create instance of nomis connector
    nomis_connector = NomisApiConnector(nomis_creds, nomis_url)

    # Check to see if a dataset already exists with this id
    dataset_exists_code = nomis_connector.get_dataset(dataset_id, return_bool=True)

    if dataset_exists_code:

        logger.info("\n-----RETRIEVING DIMENSIONS-----")
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
            logger.info("\n-----VARIABLE CREATION-----")
            for variable in query_variables:
                variable_exists_code = nomis_connector.get_variable(variable, return_bool=True)

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
            logger.info("\n-----OVERWRITING DIMENSIONS-----")
            nomis_connector.delete_dimensions(dataset_id)
            assign_dimensions_requests = ds_transformations.assign_dimensions()
            nomis_connector.assign_dimensions_to_dataset(dataset_id, assign_dimensions_requests)

        # Append observations into dataset
        logger.info("\n-----OVERWRITING OBSERVATIONS-----")
        observations_request = ds_transformations.observations(dataset_id)
        nomis_connector.overwrite_dataset_observations(dataset_id, observations_request)

        logger.info(f"\nSUCCESS: A dataset with the ID {dataset_id} has been UPDATED successfully.")

    else:
        raise Exception("A dataset with this ID does NOT exist.")


##############################


#################################################################

# ######### EXAMPLES ##########

is_update = "y"

with NomisApiConnector(config.get_credentials('nomis'), config.get_client('nomis')) as c:

    if c.get_dataset(arguments.dataset_id, return_bool=True):

        if not arguments.suppress_prompts:
            is_update = str(input(
                "--- A DATASET WITH THE ID " + arguments.dataset_id + " ALREADY EXISTS ---"
                                                                 "\n*** DO YOU WANT TO OVERWRITE/UPDATE y/n ***\n"))

        if is_update == "y":
            update_dataset(config, arguments)

        elif is_update == "n":
            logger.info("*** DATASET HAS NOT BEEN UPDATED ***")

        else:
            raise Exception("'" + is_update + "' is not a valid option. Please try again!")
    else:
        new_dataset(config, arguments)


# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
