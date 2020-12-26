from cantabular_client import LOGGER
from cantabular_client import CantabularClient
import logging
import csv
import json

class CantabularConnector:
	def __init__(self, url, creds, verify):
		self.url = url
		self.creds = creds
		self.verify = verify
		self.client = CantabularClient(self.url, self.verify)

	def connection(self):
		self.handler = logging.StreamHandler()
		self.handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
		logging.getLogger().addHandler(self.handler)
		LOGGER.setLevel(logging.INFO)

		# Create an instance of CantabularClient and pass in
		# the URL of the Cantabular server. The verify parameter
		# can be set to False to disable TLS certificate verification
		# or to the name (including path) of a CA bundle file.

		# Store your credentials in a text file with
		# a single line of the format:
		# username,password
		self.credentials = self.creds

		if len(self.credentials) != 2:
		    print('Invalid credentials fle')
		    raise Exception

		# Log in to gain access to the API. A requests.Session
		# instance is used to keep track of authentication tokens.
		try:
		    self.client.login(self.credentials[0], self.credentials[1])
		except Exception as e:
		    print("Error logging in: ", e)
		    raise
		    
		print('Successfully logged into: ', self.client.base_request)

	def query(self, variables, dataset):
		self.variables = variables
		self.dataset = dataset
		try:
		    self.cb = self.client.codebook(self.dataset, get_categories=True)
		except Exception as e:
		    print('Error getting codebook: ', e)
		    raise  

		# Perform a query using the codebook and three variables.
		# As part of the query method a call will be made to the API
		# to get detailed category information for the variables. This
		# information is stored in the codebook and reused for future
		# queries using any of the variables.https://tljh.sensiblecode.io/user/scc/kernelspecs/python3/logo-64x64.png
		try:
		    self.table = self.client.query(self.cb, variables)
		except Exception as e:
		    print('Error doing query: ', e)
		    raise

		return(self.table)