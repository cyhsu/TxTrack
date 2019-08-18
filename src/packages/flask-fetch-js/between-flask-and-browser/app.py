# docs @ http://flask.pocoo.org/docs/1.0/quickstart/

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/json',methods=['POST'])
def json_example():
    req = request.get_json()
    print(req)
    return "Thanks!"

@app.route('/hfradar/time_range/<value>', methods=['GET','POST'])
def hfradar_time_range():
    if request.method =='POST':
        data = {}
        data['start'] = value['start_date']
        data['end'] = value['end_date']
        return jsonify(data)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/')
def home():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')

app.run(debug=app.config['DEBUG'], port=4990)
