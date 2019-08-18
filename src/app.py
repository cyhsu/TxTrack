from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


###-@app.route('/_get_data/', methods=['POST'])
###-def _get_data():
###-    myList = ['Element1', 'Element2', 'Element3']
###-
###-    return jsonify({'data': render_template('response.html', myList=myList)})

@app.route('/json', methods=['POST', 'GET'])
def json_example():
	req = request.get_json()
	print(req)
	return jsonify({'data': 'Test!'})
	# return 'Test!', 200

if __name__ == "__main__":
    app.run(debug=True,port=4991)
