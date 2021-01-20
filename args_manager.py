import argparse
#filename.py {QUERY in quotes} -i {ID} -t {TITLE} -y (for yes to all prompts) -v (for verbose)

class ArgsManager:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description='Data Transformation Service Census 2021')

		self.parser.add_argument('dataset_id', action="store", help="nomis dataset ID e.g 'syn123'", type=str)
		self.parser.add_argument('dataset_title', action="store", help="nomis dataset title e.g 'TEST 1'", type=str)
		self.parser.add_argument('query_variables', action="store", help="delimited list input e.g. 'COUNTRY, SEX'", type=str)
		self.parser.add_argument('query_dataset', action="store", help="the census dataset e.g. 'Usual-Residents'", type=str)
		self.parser.add_argument('-y', action="store_true", help="suppresses all (y/n) prompts and automatically responds yes", default=False)

		self.args = self.parser.parse_args()

		self.dataset_id = self.args.dataset_id
		self.dataset_title = self.args.dataset_title
		self.query_variables = self.args.query_variables.split(", ")
		self.query_dataset = self.args.query_dataset
		self.y_flag = self.args.y
