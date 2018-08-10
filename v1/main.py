import sys
sys.path.append('../utils')

from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from mlbackend import MLBackend
from preproc import Preprocessor
import numpy as np

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

# Request parsing for validate requests.
request_parser = RequestParser(bundle_errors=True)
request_parser.add_argument("contrib_id", type=int, required=True)
request_parser.add_argument("name", type=str, required=True)
request_parser.add_argument("financial_type_id", type=int, required=True)
request_parser.add_argument("payment_instrument_id", type=int, required=True)
request_parser.add_argument("total_amount", type=float, required=True)
request_parser.add_argument("currency", type=str, required=True)
request_parser.add_argument("gateway", type=str, required=True)
request_parser.add_argument("payment_method", type=str, required=True)
request_parser.add_argument("country", type=str, required=True)
request_parser.add_argument("utm_medium", type=str, required=True)
request_parser.add_argument("utm_campaign", type=str, required=True)
request_parser.add_argument("avs_filter", type=float)
request_parser.add_argument("cvv_filter", type=float)
request_parser.add_argument("country_filter", type=float)
request_parser.add_argument("email_domain_filter", type=float)
request_parser.add_argument("utm_filter", type=float)
request_parser.add_argument("ip_filter", type=float)
request_parser.add_argument("minfraud_filter", type=float)
request_parser.add_argument("receive_date", type=str, required=True)

# Load the ML model here as a global object.
mlb = MLBackend('../private/gb-clf.pkl')

class Transaction(Resource):
	def post(self):
		args = request_parser.parse_args()

		# Preprocess the data.
		inp = Preprocessor.preprocess(args)

		# ML model evaluates transaction as fraud/not fraud.
		prob = mlb.proba_score(inp)
		res = mlb.predict(inp)
		app.logger.info('%s transaction processed.', args['contrib_id'])

		return {"proba_score" : prob, "prediction" : res};

api.add_resource(Transaction, '/transaction')

if __name__ == '__main__':
    app.run(debug=True)