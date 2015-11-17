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

	def getTableId():
		""" Get the table ID to be used for querying. """
		return table_id

	def buildQuery(prefix, suffix):
		""" Build a query with the table ID.
		:param prefix: Query fragment to append before table identification.  Trailing spaces not required.
		"param suffix: Query fragment to append after table identification.  Padding spaces not required.
		"""
		return prefix + " " + table_id + " " + suffix;

	def query(queryString):
		""" Query the BigQuery database and return results synchronously
		:param queryString: String to query BigQuery with.
		"""
		# Copy requestStructure so we don't run the risk of the structure changing
		request = requestStructure.copy()
		request['query'] = queryString
		# Convert request dict into JSON
		request = json.dumps(request)
		# Make request, takes up to request.timeoutMs
		response = service.jobs.query(project_id, request)
		# Convert returned JSON into dict for return
		return json.loads(response)

class QueryResult:
	""" Container for common methods related to BigQuery results.
	Handles determining query successes, getting the schema, and getting results from returned set."
	"""

	def __init__(self, queryResult):
		""" Initialize new QueryResult using supplied results. """
		self.queryResult = queryResult
		self.index = 0
		self.numResults = 0
		if querySuccess() is True:
			self.numResults = int(queryResult['totalRows'])
		self.numRows = len(queryResult['rows'])

	def querySuccess():
		""" Check if query was successful. """
		return queryResult['jobComplete']

	def hasErrors():
		""" Check if query returned errors or warnings. """
		return (len(queryResult['errors']) > 0)

	def resetIndex():
		""" Reset index of result feeder. """
		index = 0

	def getResults():
		""" Get query result set.
		Returns a dict of results.
		Return False for unsuccessful query.
		Return None for no results.
		"""
		if querySuccess() is True:
			return False
		if numRows == 0:
			return None
		return queryResult['rows']

	def getSchema():
		""" Get query result schema.
		Returns an array of dicts.
		"""
		if querySuccess() is False:
			return False
		return queryResult['schema']['fields']
