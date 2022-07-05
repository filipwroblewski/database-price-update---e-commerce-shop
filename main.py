from unicodedata import name
from app.database_operations import Database_operations as db
from app.api_operations import Api_operations as api

with open('resources/db login.txt', encoding='utf-8') as f:
    lines = f.readlines()
    login_db = {
        'host': lines[0].strip(),
        'user': lines[1].strip(),
        'password': lines[2].strip(),
        'database': lines[3].strip(),
    }

logging_filename = 'log.txt'
mydb = db(logging_filename=logging_filename)
mydb.db_connect(host=login_db['host'], user=login_db['user'], password=login_db['password'],
                database=login_db['database'])

myapi = api(logging_filename=logging_filename)
rates = myapi.get_rates(currencies=['eur', 'usd'])
mydb.db_update(rates=rates)
mydb.from_db_to_excel()
