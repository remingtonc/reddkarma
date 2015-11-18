from apiclient.discovery import build
import json

class BigQuery:
	""" Container for common methods related to BigQuery functionality.
	Handles BigQuery access and retrieval.
	"""

	api_key = 'AIzaSyAJn5yLJlQUx7kB2N3xEXIK_D7yEq05JJw'
	project_id = 'loyal-landing-110819'
	table_id = '[loyal-landing-110819:reddit_posts.full_corpus_201509]'

	# Basic structure of a request to the BigQuery API.
	requestStructure = {
		'timeoutMs': 10000,
		'kind': 'bigquery#queryrequest',
		'dryRun': False,
		'useQueryCahce': True,
		'defaultDataset': {
			'projectId': project_id,
			'datasetId': 'reddit_posts'
		},
		'maxResults': 100,
		'query': ''
	}

	# Build service for common usage.
	service = build('bigquery', 'v2', api_key)

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
		# Convert request dict into JSON
		# request = json.dumps(request)
		# Make request, takes up to request.timeoutMs
		response = self.service.jobs().query(projectId=self.project_id, body=request)
		# Convert returned JSON into dict for return
		return response

	def __init__(self):
		pass

class QueryResult:
	""" Container for common methods related to BigQuery results.
	Handles determining query successes, getting the schema, and getting results from returned set."
	"""

	def querySuccess(self):
		""" Check if query was successful. """
		return self.queryResult['jobComplete']

	def hasErrors(self):
		""" Check if query returned errors or warnings. """
		return (len(self.queryResult['errors']) > 0)

	def getResults(self):
		""" Get query result set.
		Returns a dict of results.
		Return False for unsuccessful query.
		Return None for no results.
		"""
		if self.querySuccess() is True:
			return False
		if self.numRows == 0:
			return None
		return self.queryResult['rows']

	def getSchema(self):
		""" Get query result schema.
		Returns an array of dicts.
		"""
		if self.querySuccess() is False:
			return False
		return self.queryResult['schema']['fields']

	def __init__(self, queryResult):
		""" Initialize new QueryResult using supplied results. """
		self.queryResult = queryResult
		self.numResults = 0
		if querySuccess() is True:
			self.numResults = int(queryResult['totalRows'])
		self.numRows = len(queryResult['rows'])
