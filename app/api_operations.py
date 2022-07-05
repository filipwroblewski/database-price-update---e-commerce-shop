import requests
import sys
from app.logging_operations import Logging_operations


class Api_operations():
    def __init__(self, logging_filename=''):
        # setting up & configuring log file
        self.log = Logging_operations(logging_filename)

    def get_rates(self, currencies=['eur', 'usd']):
        # getting current data from nbp api using json format | returning array of currencies example: [4.7096, 4.4881]
        currency_rates = []
        for currency in currencies:
            try:
                api_url = f'https://api.nbp.pl/api/exchangerates/rates/a/{currency}?format=json'
                res = requests.get(api_url).json(
                )
                currency_rates.append(res['rates'][0]['mid'])
            except requests.exceptions.JSONDecodeError as e:
                self.log.error(
                    f'{e}; given currency name: "{currency}"')
            except Exception as e:
                self.log.error(e)
                print('System exit (see logs)')
                sys.exit()

        return currency_rates
