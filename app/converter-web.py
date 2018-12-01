#!/usr/bin/python3

from flask import Flask, request, Response
import re
from converter import Converter

# Create the application instance
app = Flask(__name__)

# Create custom exception class
class CustomError(Exception):
	"""Input parameter error."""

# Create custom error handler for errors in application
@app.errorhandler(CustomError)
def handle_custom_exception(error):
	details = error.args[0]
	resp = Response(details['message'], status=200, mimetype='text/plain')
	return resp

# Create a URL route in our application for "/currency_converter"
@app.route('/currency_converter')
def currency_converter():
	"""
	This function just responds to the browser ULR
	localhost:5000/currency_converter

	:return:        the CurrencyConverter result as a JSON or an error as plain text
	"""
	amount = request.args.get('amount', type=float)
	in_currency = request.args.get('input_currency', type=str)
	out_currency = request.args.get('output_currency', type=str)

	# Validate input parameters
	if amount is None:
		raise CustomError({ 'message': 'Error: The following arguments are required: amount' })

	if re.match("^\d+?\.\d+?$", str(amount)) is None:
		raise CustomError({ 'message': 'Input parameter is invalid: Amount should be float' })

	if in_currency is None:
		raise CustomError({ 'message': 'Error: The following arguments are required: input_currency' })

	currency_converter = Converter()
	(result, error) = currency_converter.convert(amount, in_currency, out_currency)
	if result is None:
		raise CustomError({ 'message': error })
	else:
		resp = Response(result, status=200, mimetype='application/json')
		return resp

if __name__ == '__main__':
	app.run()
