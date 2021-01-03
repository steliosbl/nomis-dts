import requests
from requests.auth import HTTPBasicAuth
from pyjstat import pyjstat

class CantabularConnector:
	def __init__(self, url, creds):
		self.url = url
		self.creds = creds

		if len(self.creds) != 2:
		    raise Exception('Invalid credentials file')

	def query(self, dataset, variables):
		self.dataset = dataset
		self.variables = variables

		# Perform a query to query-json-stat endpoint using supplied BASE_URL,
		# DATASET and VARIABLES. The server is secured using HTTP Basic Authentication.
		self.QUERY = self.url + '/v8/query-json-stat/%s?%s' % (
		    self.dataset, '&'.join([f'v={v}' for v in self.variables]))

		self.response = requests.get(self.QUERY, auth=HTTPBasicAuth(self.creds[0], self.creds[1]))

		# Check for an errored response. This may occur due to network issues, if the query
		# contained invalid values, or if the entire ouput table was blocked for disclosure
		# control reasons.
		if not self.response:
		    raise Exception(f'HTTP error: {self.response.content}')

		# Load response into a pystat dataframe.
		self.table = pyjstat.Dataset.read(self.response.content.decode('utf-8'))

		# Report any categories in the rule variable that were blocked by disclosure
		# control rules.
		self.blocked_categories = self.table['extension']['cantabular']['blocked']
		if self.blocked_categories:
		    RULE_VAR_NAME, RULE_VAR = list(blocked_categories.items())[0]
		    print(f'The following categories of {RULE_VAR_NAME} failed disclosure control checks:')
		    print(', '.join(RULE_VAR['category']['label'].values()))
		    print('')


		return(self.table)