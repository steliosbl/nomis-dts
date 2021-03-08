import json
from pyjstat import pyjstat


class ReadFromFile:
    """[Description]

    :param filename:
    :type filename: str
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> pyjstat.Dataset:
        """[Description]
        :return:
        :rtype:
        """
        with open(self.filename) as json_file:
            data = json.load(json_file)
            data = json.dumps(data)

        table = pyjstat.Dataset.read(data)

        # Report any categories in the rule variable that were blocked by disclosure
        # control rules.
        blocked_categories = table['extension']['cantabular']['blocked']
        if blocked_categories:
            RULE_VAR_NAME, RULE_VAR = list(blocked_categories.items())[0]
            print(f'The following categories of {RULE_VAR_NAME} failed disclosure control checks:')
            print(', '.join(RULE_VAR['category']['label'].values()))
            print('')

        return table

# EXAMPLE

# read_from_file = readFromFile("query_file_example.json")
# table = read_from_file.read()
# print(table)
