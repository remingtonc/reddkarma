from flask import Flask, render_template, url_for
from bigquery import BigQuery, QueryResult
from werkzeug.routing import BaseConverter
import logging

logging.basicConfig(filename='reddkarma.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Application initialized')

app = Flask(__name__)
bq = BigQuery()

@app.route('/')
def home():
	return render_template('home.html', name='home')

@app.route('/r/')
def nullreddit():
	return 'No subreddit supplied.';

@app.route('/r/<subreddit>')
def subreddit(subreddit):
	return render_template('subreddit.html', name='subreddit', subreddit=subreddit)

@app.route('/queryTest')
def queryTest():
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
	for row in result.getResults():
		output += '<tr>'
		for column in row.get('f', {}):
			output += '<td>' + column.get('v', 'Null') + '</td>'
		output += '</tr>'
	output += '</table>'
	return output
