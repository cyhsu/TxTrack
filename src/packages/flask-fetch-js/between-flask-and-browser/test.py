from flask import Flask, jsonify, request, render_template
import sys

app = Flask(__name__)


@app.route("/function_route", methods=["GET", "POST"])
def my_function():
    if request.method == "POST":
     data = {} #// empty dict to store data
     data['title'] = request.json['title']
     data['release_date'] = request.json['movie_release_date']

     #// do whatever you want with the data here e.g look up in database or something
     #// if you want to print to console

     print(data, file=sys.stderr)

     #// then return something back to frontend on success

     #// this returns back received data and you should see it in browser console
     #// because of the console.log() in the script.
     return jsonify(data)
    else:
     return render_template('the_page_i_was_on.html')



app.run(port=4990)
