import os
from helpers.file_manager import FileManager
from helpers.format_converter import FormatConverter
from helpers.query import Query
from helpers.pre_process import pre_process_and_query 
from flask import Flask, render_template, jsonify, request
from time import sleep

global q
global numFiles

app = Flask(__name__)

@app.route("/")
def index():
	"""
	Initial setup for flask app
	:return:
	"""
	#pre_process_and_query()
	return render_template("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
	"""
	"""
	try:
		if request.method == 'GET':
			print(request)
			query = request.args.get('query')
			print(query)
			# query pre-processing
			q.query_preprocess(query)

			#print("Preprocessing done")
			# displaying resutls
			q.display_results(numFiles)
			ans, rank = q.results, 1
			ans.sort()
			ans = ans[::-1][0:3]

			#print("Results:\n", ans)
			ranked_results = {}
			for element in ans:
				if element[0] > 0:
					ranked_results[str(rank)] = q.preprocessor.fileNames[element[1]]
					rank += 1
			#print("end")
			return jsonify(ranked_results)
			   
	except Exception as e:
		return (e)


if __name__=='__main__':
	q,numFiles = pre_process_and_query()
	sleep(5)
	print("Server Start")
	app.run(host='0.0.0.0', port=5002, debug=True, threaded=True, use_reloader=False)
