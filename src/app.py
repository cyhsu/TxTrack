from flask import Flask, render_template, jsonify, request
from src.api.fetch import fetch

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trajectory', methods=['POST', 'GET'])
def json_example():
    req = request.get_json()
    # print('\n\n\n\n')
    print('\n\t\t','Get Json from Javascripts')
    print('\t\t',req,'\n')
    SiteLon, SiteLat = float(req['lon']), float(req['lat'])
    SiteStartTime, SiteEndTime = req['start_time'][:-5], req['end_time'][:-5]
    cls = fetch(SiteLon, SiteLat, SiteStartTime, SiteEndTime)
    output = cls.json()
    print('\n')
    print('\n\t\t','Post new Json to Javascripts')
    print('\t\t', output,'\n')
    # return output
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True,port=4991)
