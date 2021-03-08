import argparse


# filename.py {QUERY in quotes} -i {ID} -t {TITLE} -y (for yes to all prompts) -v (for verbose)


class ArgsManager:
    """Class for handling the input arguments, utilising the argparse library module. Allows for command line arguments
    in the form: filename.py {QUERY in quotes} -i {ID} -t {TITLE} -y (for yes to all prompts) -v (for verbose)

    """

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description='Data Transformation Service Census 2021')

        parser.add_argument('query_variables', action="store", help="delimited list input e.g. 'COUNTRY, SEX'",
                            type=str)
        parser.add_argument('-i', '--dataset-id', action="store", help="nomis dataset ID e.g 'syn123'", type=str)
        parser.add_argument('-t', '--dataset-title', action="store", help="nomis dataset title e.g 'TEST 1'",
                            type=str)
        parser.add_argument('-d', '--query-dataset', action="store",
                            help="the census dataset e.g. 'Usual-Residents'", type=str)
        parser.add_argument('-y', '--suppress-prompts', action="store_true",
                            help="suppresses all (y/n) prompts and automatically responds yes", default=False)
        parser.add_argument('-v', '--verbose', action="store_true", help="verbose", default=False)
        parser.add_argument('-f', '--filename', action="store",
                            help="read data from a file instead of querying cantabular", type=str, default=None)
        parser.add_argument('-c', '--config', action="store", help="path for non-default config file",
                            default=None, type=str)

        args = parser.parse_args()

        self.query_variables = args.query_variables.split(", ")
        self.dataset_id = args.dataset_id
        self.dataset_title = args.dataset_title
        self.query_dataset = args.query_dataset
        self.y_flag = args.suppress_prompts
        self.v_flag = args.verbose
        self.filename = args.filename

        if args.config is not None:
            self.config = True
            self.config_path = args.config
        else:
            self.config = False
            self.config_path = None

        # Toggle Bool indicating if a file is used for the metadata; will evaluate to False by default
        self.use_file = True if self.filename is not None else False
