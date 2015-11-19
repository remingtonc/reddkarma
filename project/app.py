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

@app.route('/potential')
def potential():
	preQuery = 'SELECT subreddit as Subreddit, MAX(median) as Potential FROM (SELECT subreddit, PERCENTILE_CONT(0.5) OVER (PARTITION BY subreddit ORDER BY score) as median FROM'
	postQuery = 'GROUP BY Subreddit ORDER BY Potential DESC LIMIT 20'
	queryString = bq.buildQuery(preQuery, postQuery)
	result = bq.query(queryString)
	result = QueryResult(result)
	return result.getHTMLTable()

@app.route('/queryTest')
def queryTest():
	preQuery = 'SELECT domain, COUNT(*) count, ROUND(AVG(score), 1) avg_score FROM'
	postQuery = 'WHERE YEAR(SEC_TO_TIMESTAMP(created))=2015 AND NOT domain CONTAINS "self." GROUP BY 1 HAVING count > 700 ORDER BY 3 DESC LIMIT 10'
	queryString = bq.buildQuery(preQuery, postQuery)
	result = bq.query(queryString)
	result = QueryResult(result)
	return result.getHTMLTable()