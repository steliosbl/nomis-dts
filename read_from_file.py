import json
from pyjstat import pyjstat

class ReadFromFile:
	def __init__(self, filename):
		self.filename = filename

	def read(self):

		with open(self.filename) as json_file:
			self.data = json.load(json_file)
			self.data = json.dumps(self.data)

		self.table = pyjstat.Dataset.read(self.data)

		# Report any categories in the rule variable that were blocked by disclosure
		# control rules.
		self.blocked_categories = self.table['extension']['cantabular']['blocked']
		if self.blocked_categories:
		    self.RULE_VAR_NAME, self.RULE_VAR = list(self.blocked_categories.items())[0]
		    print(f'The following categories of {self.RULE_VAR_NAME} failed disclosure control checks:')
		    print(', '.join(self.RULE_VAR['category']['label'].values()))
		    print('')

		return(self.table)


# EXAMPLE

# read_from_file = readFromFile("query_file_example.json")
# table = read_from_file.read()
# print(table)