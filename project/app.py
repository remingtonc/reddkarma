from flask import Flask
import bigquery

app = Flask(__name__)
bq = BigQuery()

SELECT domain, COUNT(*) count, ROUND(AVG(score), 1) avg_score
FROM [fh-bigquery:reddit_posts.full_corpus_201509]
WHERE YEAR(SEC_TO_TIMESTAMP(created))=2015
AND NOT domain CONTAINS 'self.'
GROUP BY 1
HAVING count>700
ORDER BY 3 DESC
LIMIT 100

@app.route('/')
def home():
	preQuery = 'SELECT domain, COUNT(*) count, ROUND(AVG(score), 1) avg_score FROM'
	postQuery = 'WHERE YEAR(SEC_TO_TIMESTAMP(created))=2015 AND NOT domain CONTAINS "self."" GROUP BY 1 HAVING count > 700 ORDER BY 3 DESC LIMIT 10'
	queryString = bq.buildQuery(preQuery, postQuery)
	result = bq.query(queryString)
	result = QueryResult(result)
	if (!result.querySuccess()):
		return 'Query did not succeed.'
	output = '<table><tr>'
	headers = result.getSchema()
	while (header = headers.next()):
		output += '<th>' + header['name'] + '</th>'
	output += '</tr>'
	while (row = result.getResult()):
		output += '<tr>'
		while (val = row.next()):
			output += '<td>' + val + '</td>'
		output += '</tr>'
	output += '</table>'
	return output
