#!/usr/bin/python3

from flask import Flask, request, Response
import re
from converter import Converter

app = Flask(__name__)

class InputParameterError(Exception):
	"""Input parameter error."""

class CurrencyException(Exception):
	"""Currency interpetation error."""

@app.errorhandler(CurrencyException)
def handle_currency_exception(error):
	details = error.args[0]
	resp = Response(details['message'], status=200, mimetype='text/plain')
	return resp

@app.errorhandler(InputParameterError)
def handle_input_parameter_error(error):
	details = error.args[0]
	resp = Response('Input parameter is invalid: ' + details['message'], status=200, mimetype='text/plain')
	return resp

@app.route('/currency_converter')
def currency_converter():
	amount = request.args.get('amount', type=float)
	in_currency = request.args.get('input_currency', type=str)
	out_currency = request.args.get('output_currency', type=str)

	# Validate amount parameter
	if re.match("^\d+?\.\d+?$", str(amount)) is None:
		raise InputParameterError({ 'message': 'Amount should be float' })

	currency_converter = Converter()
	(result, error) = currency_converter.convert(amount, in_currency, out_currency)
	if result is None:
		raise CurrencyException({ 'message': error })
	else:
		resp = Response(result, status=200, mimetype='application/json')
		return resp

if __name__ == '__main__':
	app.run()
