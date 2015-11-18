from flask import Flask
from bigquery import BigQuery, QueryResult
import logging

logging.basicConfig(filename='reddkarma.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Debug message check.')

app = Flask(__name__)
bq = BigQuery()

@app.route('/')
def home():
	preQuery = 'SELECT domain, COUNT(*) count, ROUND(AVG(score), 1) avg_score FROM'
	postQuery = 'WHERE YEAR(SEC_TO_TIMESTAMP(created))=2015 AND NOT domain CONTAINS "self." GROUP BY 1 HAVING count > 700 ORDER BY 3 DESC LIMIT 10'
	queryString = bq.buildQuery(preQuery, postQuery)
	result = bq.query(queryString)
	result = QueryResult(result)
	if result.querySuccess() is not True:
		return 'Query did not succeed.'
	output = '<table><tr>'
	headers = result.getSchema()
	for header in headers:
		output += '<th>' + header['name'] + '</th>'
	output += '</tr>'
	for row,rowvalue in result.getResults():
		output += '<tr>'
		for column,columnvalue in rowvalue:
			output += '<td>' + columnvalue + '</td>'
		output += '</tr>'
	output += '</table>'
	return output
