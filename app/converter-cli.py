#!/usr/bin/python3
"""CLI script for testing currency converter
"""
from converter import Converter
import re
import argparse

parser = argparse.ArgumentParser()

def main():
	parser.add_argument('--amount', required=True, type=float)
	parser.add_argument('--input_currency', required=True, type=str)
	parser.add_argument('--output_currency', required=False, type=str)
	args = parser.parse_args()

	amount = args.amount
	in_currency = args.input_currency
	out_currency = args.output_currency

	currency_converter = Converter()
	(result, error) = currency_converter.convert(amount, in_currency, out_currency)
	if not result is None:
		print(result)
	else:
		print(error)

if __name__ == "__main__":
	main()
