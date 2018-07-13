from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from mlbackend import MLBackend as MLB

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

# Request parsing for validate requests.
request_parser = RequestParser(bundle_errors=True)
request_parser.add_argument("arg1", type=str, required=True, help="Testing")

# Load the ML model here as a global object.

class Transaction(Resource):
	def validate(self):
		args = request_parser.parse_args()

		# Preprocess the data.
		# trans_data = MLBackend.preprocess(args)

		# ML model evaluates transaction as fraud/not fraud.
		# MLBackend.predict(trans_data)

		return {"fraud" : False};

api.add_resource(Transaction, '/transaction')

if __name__ == '__main__':
    app.run(debug=True)