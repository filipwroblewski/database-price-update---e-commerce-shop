# Database price update - e-commerce shop

### Project video presentation

[![YouTube video](http://img.youtube.com/vi/u_b8ghru2xA/0.jpg)](http://www.youtube.com/watch?feature=player_embedded&v=u_b8ghru2xA)

## The description of end-user’s requirement

The seller has an e-commerce store with various products. Until now, the trade was carried out only in Poland. The seller wanted to distribute the products to European Union countries and the United States. Therefore, they needed to accept payments in American dollars (USD) and in Euro. The buyer needs to know how much the goods cost in a given currency.

The seller needs a tool that will once a day or if requested download the current exchange rate from the National Bank of Poland and update the prices of the products in a database.

## Configuration

_cmd_

```cmd
pip install mysql-connector-python
```

1. Install MySQL database and create database with name **mydb**.
2. Import [schema](https://github.com/filipwroblewski/database-price-update---e-commerce-shop/blob/main/resources/schema.sql) of e-commerce shop to mydb.
3. Import [test data](https://github.com/filipwroblewski/database-price-update---e-commerce-shop/blob/main/resources/data.sql) to mydb
   _Comment: data have to be loaded from top to bottom, transaction after transaction, to avoid import error._

## Functional requirements

1. In the table named Product, add two columns: UnitPriceUSD, UnitPriceEuro.

   _sql_

   ```sql
   ALTER TABLE `mydb`.`Product`
   ADD UnitPriceUSD DECIMAL;

   ALTER TABLE `mydb`.`Product`
   ADD UnitPriceEuro DECIMAL;
   ```

2. Write a Python script that will connect to the National Bank of Poland via the REST API and will download the current exchange rate for USD and Euro. API for the NBP is linked here: _http://api.nbp.pl/en.html_.

   _cmd_

   ```cmd
   pip install requests
   ```

   _python_

   ```py
   import requests

   res = requests.get('https://excample_url?format=json').json()
   print(len(res.text))
   ```

3. After downloading the courses, the script should update the prices of all the products in the database (columns: UnitPriceUSD, UnitPriceEuro).

   _cmd_

   ```cmd
   pip install mysql-connector-python
   ```

   _python_

   ```py
   import mysql.connector

   mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
   ```

4. Then the script should have a separate mode of operation, which it will generate on request an [Excel spreadsheet](https://github.com/filipwroblewski/database-price-update---e-commerce-shop/blob/main/products.xlsx) with a list of all the products in the database in the columns: **ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice, UnitPriceUSD, UnitPriceEuro, Ranking**

![Excel img](https://img.youtube.com/vi/u_b8ghru2xA/3.jpg)

   _cmd_

   ```cmd
   pip install xlsxwriter
   ```

   _python_

   ```py
   workbook = xlsxwriter.Workbook(filename)
   worksheet = workbook.add_worksheet()
   for i in range(len(elems)):
      worksheet.write(row, col + i, elems[i])
   row += 1
   workbook.close()
   ```

## Non-functional requirements:

1. The script should be object-oriented.
2. The script’s code should be documented.
3. The solution should be uploaded to a GitHub account.
4. Changed [database schema](https://github.com/filipwroblewski/database-price-update---e-commerce-shop/blob/main/resources/database%20schema.sql) should be exported as sql and also uploaded to GitHub.
5. The script should use the logging module to log the operation from activity to [log file](https://github.com/filipwroblewski/database-price-update---e-commerce-shop/blob/main/log.txt).
6. The script should also handle exceptions, eg when the NBP API is not available or as a base the data will not be available or as another errors occur. All errors should be logged to the log file.
