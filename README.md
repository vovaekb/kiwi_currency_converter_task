# kiwi_currency_converter_task
Currency converter program:

- CLI application
- Web API application

Client scripts: 

converter-cli.py and converter-web.py. converter.py comprises the logic of the currency converter. 

currencies.json contains mapping between currency codes and symbols.

## Installation
### Requirements
* Python 3
* Docker 

### Deployment using Dockerfile
For deployment on production Dockerfile is provided. Build image from the Dockerfile:
```bash
docker build . -t currency-converter
```

Run the currency-converter image:
```bash
docker run currency-converter
```

## CLI client
CLI client is represented by converter-cli.py. To run CLI application:

```bash
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
```
--amount and --input_currency arguments are required, --output_currency argument is optional. If --output_currency is missing, amount will be converted to all known currencies.

## Web client
Web API client is represented by converter-web.py. 
Flask using Python 2.7 on default. To run web application using Python 3:
```bash
./converter-web.py
```
Open following URL in browser:
```bash
http://127.0.0.1:5000/currency_converter?amount=20&&input_currency=RUB&&output_currency=CZK
```
amount and input_currency arguments are required, output_currency argument is optional. If output_currency is missing, amount will be converted to all known currencies.
