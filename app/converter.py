"""Currency Converter Class

This script allows the user to convert between different currencies.

This script requires that `forex-python` be installed within the Python environment you are running this script in.

This file can be imported as a module and contains the class Converter.
"""
from forex_python.converter import CurrencyRates
import simplejson as json
import sys

class IncorrectCurrencyError(Exception):
	"""Incorrect currency specified"""

class MultipleCurrenciesError(Exception):
	"""Many currencies use the specified symbol"""

class Converter:
	"""
	Basic class used to convert currencies.

	...

	Attributes
	----------
	symbol_code_map : dictionary
		a map between currency symbols and codes

	Methods
	-------
	convert(amount, in_currency, out_currency=None)
		Performs conversion between currencies
	
	load_currencies()
		Loads currencies from JSON file
	
	
	get_currency_code(symbol)
		Finds code of currency using specific symbol
	
	get_rate(amount, in_currency, out_currency)
		Performs conversion of amount from in_currency to out_currency
	"""
	def __init__(self):
		self.symbol_code_map = {}
		self.load_currencies()

	def load_currencies(self):
		"""
		Method loading currencies and creating mapping between their symbols and codes
		"""
		with open('currencies.json') as f:
			currency_data = json.load(f)
			self.symbol_code_map = {str(cur['cc']): cur['symbol'].encode('utf-8') for cur in currency_data}

	def get_rate(self, amount, in_currency, out_currency):
		"""
		Performs conversion of amount from in_currency to out_currency

		Parameters
		----------
		amount : int
			amount to convert

		in_currency : str
			The currency to convert from

		out_currency : str
			The currency to convert to

		Returns
		-------
		rate : float
			the conversion result
		"""
		rates = CurrencyRates()
		try:
			rate = rates.convert(in_currency, out_currency, amount)
		except:
			return None
		return rate

	def get_currency_code(self, currency_symbol):
		"""
		Finds codes of currencies using specific symbol

		Parameters
		----------
		currency : str
			a currency symbol to find a code for

		Returns
		-------
		currency_code : str
			a currency code corresponding to the input currency symbol

		Raises
		------
		IncorrectCurrencyError
			If the currency code is not found for the symbol specified

		MultipleCurrenciesError
			If many currencies use the symbol specified
		"""
		symbol = currency_symbol.encode('utf-8')
		codes = [cc for cc in self.symbol_code_map if self.symbol_code_map[cc] == symbol]
		
		if not codes:                                                                                        
			# currency is not correct: no currency code found for the input
			raise IncorrectCurrencyError({ 'message': 'Currency is not correct' })
		elif len(codes) > 1:
			# many currencies use this symbol
			raise MultipleCurrenciesError({'message': 'Many currencies use the symbol {}: {}. Please choose correct one.'.format(currency_symbol, ', '.join(codes)) })
		else:                                                                                                
			# code is found                                                                              
			currency_code = codes[0]
			return currency_code

	def convert(self, amount, in_currency, out_currency=None):
		"""
		Method implementing conversion between currencies.

		If the argument output_currency isn't passed in, the method converts input_currency to all known currencies.

		Parameters
		---------
		amount : int
			The amount to convert
		in_currency : str
			The currency to convert from
		out_currence : str, optional
			The currency to convert to

		Returns
		-------
		result : json
			result of currency conversion
		"""
		result = None
		in_currency_code = in_currency
		
		# symbol is specified for input currency
		if not in_currency in self.symbol_code_map:
			try:
				in_currency_code = self.get_currency_code(in_currency)
			except IncorrectCurrencyError as e:
				# Currency code not found
				details = e.args[0]
				return (None, 'Input currency error: ' + details['message'])
			except MultipleCurrenciesError as e:
				# Many currencies use the symbol
				details = e.args[0]
				return (None, 'Input currency error: ' + details['message'])
		
		out_data = {}
		out_data['input'] = { "amount": amount, "currency": in_currency_code }

		if out_currency is None:
			# convert in_currency to all known currencies
			out_data['output'] = {}

			for currency_code in filter(lambda x: x != in_currency_code, self.symbol_code_map): 
				rate = self.get_rate(amount, in_currency_code, currency_code)
				
				if rate is None:
					out_data['output'][currency_code] = 'Error in obtaining rate'
				else:
					out_data['output'][currency_code] = rate
		else:
			# convert in_currency to out_currency
			out_currency_code = out_currency
			if not out_currency in self.symbol_code_map:   
				# Look for the code for the currency symbol specified
				try:
					out_currency_code = self.get_currency_code(out_currency)
				except IncorrectCurrencyError as e:
					# Currency code not found
					details = e.args[0]
					return (None, 'Output currency error: ' + details['message'])
				except MultipleCurrenciesError as e:
					# Many currencies use the symbol
					details = e.args[0]
					return (None, 'Output currency error: ' + details['message'])

			# Perform conversion
			rate = self.get_rate(amount, in_currency_code, out_currency_code)

			if rate is None:
				out_data['output'] = { 'Error': 'Error in obtaining rate' }
			else:
				out_data['output'] = { out_currency_code: rate }

		# Create JSON for the result and return it
		json_data = json.dumps(out_data, sort_keys=True, indent=4 * ' ')
		return (json_data, None)
