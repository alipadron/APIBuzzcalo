"""dev: franco@systemagency.com

For execute this python script:
$ python3 app.py

This script will active a web server to response the
requests from endpount | route ''.
"""

import os

from flask import Flask
from flask_cors import CORS, cross_origin
from flask import render_template, redirect, url_for
from flask import session, request, jsonify, make_response

import decimal
import flask.json
from dotenv import load_dotenv
# load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from model.Articulo import Articulo
from route.Reporte import reporte


app = Flask(__name__)

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app.json_encoder = MyJSONEncoder

# Init the decorator for authentication
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
# Grant access on CORS
CORS(app)

# Registration of the set of endpoints.
app.register_blueprint(reporte)


@app.route('/', methods=['GET'])
def main_login():
    template = 'reporte/AmazonMeli.html'
    data = {}

    return render_template(template, data=data), 200


if __name__ == '__main__':
    app.run(port=8000)
    # app.run(host='0.0.0.0', port='443')
