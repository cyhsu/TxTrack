import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html')

@app.route("/json", methods=["POST"])
def json_example():
	if request.method == 'POST':
		req = request.json
		print('112233',req)
		return "Test!", 200,


if __name__ == '__main__':
	# run!
	app.run()
