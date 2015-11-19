from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
import secrets
import logging

class BigQuery:
	""" Container for common methods related to BigQuery functionality.
	Handles BigQuery access and retrieval.
	"""

	api_key = secrets.api_key
	project_id = secrets.project_id
	table_id = secrets.table_id

	# Basic structure of a request to the BigQuery API.
	requestStructure = {
		'timeoutMs': 10 * 1000,
		'kind': 'bigquery#queryRequest',
		'dryRun': False,
		'useQueryCache': True,
		'defaultDataset': {
			'projectId': project_id,
			'datasetId': 'reddit_posts'
		},
		'maxResults': 100,
		'query': ''
	}

	# Grab the application's default credentials from the environment.
	credentials = GoogleCredentials.get_application_default()
	# Build service for common usage across instances.
	service = build('bigquery', 'v2', credentials=credentials)

	def getTableId(self):
		""" Get the table ID to be used for querying. """
		return self.table_id

	def buildQuery(self, prefix, suffix):
		""" Build a query with the table ID.
		:param prefix: Query fragment to append before table identification.  Trailing spaces not required.
		"param suffix: Query fragment to append after table identification.  Padding spaces not required.
		"""
		return prefix + " " + self.table_id + " " + suffix;

	def query(self, queryString):
		""" Query the BigQuery database and return results synchronously
		:param queryString: String to query BigQuery with.
		"""
		# Copy requestStructure so we don't run the risk of the structure changing
		request = self.requestStructure.copy()
		request['query'] = queryString
		# Make request, takes up to request.timeoutMs
		try:
			response = self.service.jobs().query(projectId=self.project_id, body=request).execute()
		except HttpError as e:
			logging.error('Error: {}'.format(e.content))
			raise e
		return response

	def __init__(self):
		pass

class QueryResult:
	""" Container for common methods related to BigQuery results.
	Handles determining query successes, getting the schema, and getting results from returned set.
	"""

	def querySuccess(self):
		""" Check if query was successful. """
		return self.queryResult.get('jobComplete', False)

	def hasErrors(self):
		""" Check if query returned errors or warnings. """
		return (len(self.queryResult.get('errors', []) > 0))

	def getResults(self):
		""" Get query result set.
		Returns a dict of results.
		Return False for unsuccessful query.
		Return None for no results.
		"""
		if self.querySuccess() is False:
			return False
		if self.numRows == 0:
			return None
		return self.queryResult.get('rows', {})

	def getSchema(self):
		""" Get query result schema.
		Returns an array of dicts.
		"""
		if self.querySuccess() is False:
			return False
		return self.queryResult.get('schema', {'fields': {}}})['fields']

	def __init__(self, queryResult):
		""" Initialize new QueryResult using supplied results. """
		self.queryResult = queryResult
		self.numResults = 0
		if self.querySuccess() is True:
			self.numResults = int(queryResult.get('totalRows', 0))
		self.numRows = len(queryResult.get('rows', []))
