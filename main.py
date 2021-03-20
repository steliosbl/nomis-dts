from nomis_metadata_api_connector import NomisMetadataApiConnector
from cantabular_api_connector import CantabularApiConnector
from dataset_transformations import DatasetTransformations
from dataset_file_reader import DatasetFileReader
from nomis_api_connector import NomisApiConnector
from config_manager import ConfigManager
from configuration import Configuration
from args_manager import ArgsManager
from file_reader import FileReader
from type_hints import *
from arguments import Arguments
from pyjstat import pyjstat
import logging
import sys

# ---------- Initialisation ---------- #


# Initialise logging

logger = logging.getLogger('DTS-Logger')
logger.propagate = False
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s; in %(filename)s] %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
file_handler = logging.FileHandler("dts.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Collect arguments
def collect_arguments() -> Arguments:
    """Use the Args Manager to establish the arguments for this run
    """

    with ArgsManager() as am:
        arguments = am.decode_arguments()

    if arguments.verbose:
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

    if arguments.log_file is not None:
        logger.handlers.remove(file_handler)
        new_file_handler = logging.FileHandler(arguments.log_file)
        new_file_handler.setFormatter(formatter)
        logger.addHandler(new_file_handler)

    return arguments


# Establish configuration
def collect_configuration(arguments: Arguments) -> Configuration:
    """Use the Config Manager to establish the configuration for this run
    """

    with ConfigManager(arguments) as cm:
        configuration = cm.decode_configuration()

    return configuration


# ---------- Data Functions ---------- #


def check_dataset_exists(connector: NomisApiConnector) -> bool:
    """Check whether the dataset already exists in the Nomis database, handle appropriately
    """
    exists = connector.get_dataset(args.dataset_id, return_bool=True)
    if exists and not args.suppress_prompts:
        print(f"A DATASET WITH ID {args.dataset_id} ALREADY EXISTS. DO YOU WANT TO UPDATE IT? y/n")
        while 1:
            answer = input()
            if answer.lower() == 'n':
                print("DATASET HAS NOT BEEN UPDATED")
                sys.exit(0)
            elif answer.lower() == 'y':
                break
            print("PLEASE INPUT EITHER 'y' (YES) OR 'n' (NO)")
    return exists


def retrieve_data() -> Tuple[pyjstat.Dataset, List[str]]:
    """Query the Cantabular API to retrieve a jsonstat table for use in dataset construction and transformation
    """
    if args.filename is not None:
        with DatasetFileReader(args.filename) as dfr:
            table = dfr.query()
            variables = table['id']
    else:
        with CantabularApiConnector(
                args.query_dataset,
                args.query_variables,
                config.get_credentials('cantabular'),
                config.get_client('cantabular'),
        ) as cc:
            table = cc.query()
            variables = args.query_variables
    return table, variables


def get_non_assigned_variables(connector: NomisApiConnector
                               ) -> List[str]:
    """Obtain a list of all variables marked for posting that haven't already been assigned to the dataset
    """

    assigned_variables_json = connector.get_dataset_dimensions(args.dataset_id)
    assigned_variables = [assigned_variables_json[i]['name'] for i in range(len(assigned_variables_json))]

    # Check to see if any of the variables in the observation request
    non_assigned_variables = [variable for variable in args.query_variables if variable not in assigned_variables]

    return non_assigned_variables

def get_type_ids(type_requests) -> List[str]:
    """Obtain a list of all unique type ID
    """

    type_ids = []
    for request in type_requests:
        type_ids.append(request["id"])

    return type_ids

def create_dataset(connector: NomisApiConnector,
                   transformations: DatasetTransformations
                   ) -> None:
    """Initialise a dataset using the jsonstat table either read in or retrieved from Cantabular
    """
    connector.create_dataset(
        args.dataset_id,
        transformations.dataset_creation(
            args.dataset_id,
            args.dataset_title
        )
    )


def handle_variables(connector: NomisApiConnector,
                     transformations: DatasetTransformations,
                     variables: List[str]
                     ) -> None:
    """Handle variable transmission/manipulation
    """

    logger.info("\n-----VARIABLE CREATION-----")

    # Create the variable creation and category request bodies
    variable_request_body = transformations.variable_creation()
    type_request_body = transformations.type_creation()
    type_ids = get_type_ids(type_request_body)
    category_request_body = transformations.category_creation(type_ids)

    for variable in variables:

        # Check to see variables already exist for the given dimensions; IF the variable does NOT exist then create it
        if not connector.get_variable(variable, return_bool=True):

            # Create variable
            for request in variable_request_body:
                if request["name"] == variable:
                    connector.create_variable(variable, request)

            # Create variable type
            requests = []
            for request in type_request_body:
                if request["reference"] == variable:
                    requests.append(request)
            connector.create_variable_type(variable, requests)

            # Create the categories for this new variable
            requests = []
            for category in transformations.table["dimension"][variable]["category"]["index"]:
                for request in category_request_body:
                    if category == request["code"] and transformations \
                            .table["dimension"][variable]["category"]["label"][category] == request["title"]:
                        requests.append(request)

            connector.create_variable_category(variable, requests)


# Assign dimensions to dataset
def handle_dimensions(connector: NomisApiConnector,
                      transformations: DatasetTransformations
                      ) -> None:
    """Assign dimensions to the dataset
    """

    logger.info("\n-----ASSIGNING DIMENSIONS-----")
    connector.assign_dimensions_to_dataset(
        args.dataset_id,
        transformations.assign_dimensions()
    )


# Append observations into dataset
def handle_observations(connector: NomisApiConnector,
                        transformations: DatasetTransformations
                        ) -> None:
    """Append/overwrite observations to the dataset
    """

    logger.info("\n-----APPENDING OBSERVATIONS-----")
    connector.overwrite_dataset_observations(
        args.dataset_id,
        transformations.observations(args.dataset_id)
    )


def dataset_transformations(connector: NomisApiConnector,
                            exists: bool,
                            data: Tuple[pyjstat.Dataset, List[str]]
                            ) -> None:
    """Function containing the dataset transformation operations
    """

    table, variables = data
    transformations = DatasetTransformations(table)

    # Create the dataset if it doesn't exist, otherwise retrieve the non-assigned variables
    if not exists:
        non_assigned_variables = variables
        create_dataset(connector, transformations)
    else:
        non_assigned_variables = get_non_assigned_variables(connector)

    # Create any new variables and assign all non assigned variables to the dataset
    if len(non_assigned_variables) > 0:
        handle_variables(connector, transformations, variables)
    handle_dimensions(connector, transformations)
    handle_observations(connector, transformations)


# ---------- Metadata Functions ---------- #


def cantabular_metadata(file_data: dict) -> List[UuidMetadata]:
    """Function for handling metadata in the Cantabular format
    """

    # Extract variable IDs
    data = [meta["meta"] for meta in file_data["vars"]]
    variables = [meta["id"] for meta in file_data["vars"]]
    uuids_metadata: List[UuidMetadata] = []

    # Get UUIDs from Nomis
    with NomisApiConnector(
            config.get_credentials('nomis'),
            config.get_client('nomis')
    ) as connector:
        for variable in range(0, len(variables)):

            response = connector.get_variable(
                variables[variable],
                return_bool=True
            )

            if response is not False:
                uuids_metadata.append(UuidMetadata(response["uuid"], data[variable]))

    return uuids_metadata


def ons_metadata(file_data: dict) -> List[UuidMetadata]:
    """Function for handling metadata in the ONS format
    """

    # Get a list of all UUIDs in the Nomis system
    with NomisApiConnector(
            config.get_credentials('nomis'),
            config.get_client('nomis')
    ) as connector:
        nomis_uuids = [variable["uuid"] for variable in connector.get_variable()]

    uuids_metadata: List[UuidMetadata] = []

    # Extract UUIDs and metadata
    for meta in file_data["dataModel"]["dataTypes"]:

        # Check if the UUIDs match those in the Nomis system; otherwise, skip
        if meta["id"] in nomis_uuids:
            uuids_metadata.append(UuidMetadata(meta["id"], {"description": meta["description"]}))
        else:
            logger.info(f"{meta['label']} with UUID {meta['id']} does not exist in NOMIS system")

    for meta_x in file_data["dataModel"]["childDataClasses"]:

        # Check other variable branches
        for meta_y in meta_x["childDataElements"]:

            # Check if the UUIDs match those in the Nomis system; otherwise, skip
            if meta_y["id"] in nomis_uuids:
                uuids_metadata.append(UuidMetadata(meta_y["id"], {"description": meta_y["description"]}))
            else:
                logger.info(f"VARIABLE: '{meta_y['label']}' with UUID: '{meta_y['id']}' does not exist in NOMIS system")

    return uuids_metadata


# ---------- Main Functions ---------- #


def data_main() -> None:
    """Main function for handling datasets
    """

    with NomisApiConnector(
            config.get_credentials('nomis'),
            config.get_client('nomis')
    ) as connector:
        exists = check_dataset_exists(connector)
        dataset_transformations(connector, exists, retrieve_data())
    logger.info(f"SUCCESS: A dataset with the ID {args.dataset_id} has been "
                f"{'UPDATED' if exists else 'CREATED'} successfully.")


def metadata_main() -> None:
    """Main function for handling metadata
    """

    with FileReader(args.filename) as fr:
        file_data = fr.load_json()
    if args.metadata_format.lower() == 'c':
        uuids_metadata = cantabular_metadata(file_data)
    elif args.metadata_format.lower() == 'o':
        uuids_metadata = ons_metadata(file_data)
    else:
        raise ValueError("Unrecognised metadata format.")

    if len(uuids_metadata) > 0:
        variable_metadata_requests = DatasetTransformations.variable_metadata_request(uuids_metadata)
        # print(json.dumps(variable_metadata_requests, indent=2))
        with NomisMetadataApiConnector(
                config.get_credentials('nomis_metadata'),
                config.get_client('nomis_metadata')
        ) as metadata_connector:
            uuids = metadata_connector.add_new_metadata(variable_metadata_requests, return_uuids=True)
        logger.info(f"Metadata handled successfully. {uuids}")

    else:
        logger.info("No metadata appended.")


if __name__ == '__main__':
    args = collect_arguments()
    config = collect_configuration(args)
    data_main() if not args.metadata else metadata_main()
