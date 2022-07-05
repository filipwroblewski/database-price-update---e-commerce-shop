import sys
import mysql.connector
import xlsxwriter
from app.logging_operations import Logging_operations


class Database_operations():
    def __init__(self, logging_filename=''):
        # setting up & configuring log file
        self.log = Logging_operations(logging_filename)

    def db_connect(self, host, user, password, database):
        # connecting & creating connector to database
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        except mysql.connector.Error as e:
            self.log.error(e)
            sys.exit()

    def db_update(self, rates, columns=['UnitPriceUSD', 'UnitPriceEuro']):
        # updating all prices in Procuct table, with given currency rates
        try:
            for i in range(len(rates)):
                mycursor = self.mydb.cursor()
                sql = f"UPDATE `mydb`.`Product` SET {columns[i]} = UnitPrice / {rates[i]}"
                mycursor.execute(sql)
                self.mydb.commit()
                self.log.info(
                    f"Updated {mycursor.rowcount} record(s), in {columns[i]} column")
        except Exception as e:
            self.log.error(e)

    def from_db_to_excel(self, filename='products.xlsx', column_names=['ProductID', 'DepartmentID', 'Category', 'IDSKU', 'ProductName',
                                                                       'Quantity', 'UnitPrice', 'UnitPriceUSD', 'UnitPriceEuro', 'Ranking']):
        # creating excel file, based on Product table column names

        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(
                f"SELECT {', '.join(column_names)} FROM `mydb`.`Product`")
            myresult = mycursor.fetchall()
        except Exception as e:
            self.log.error(e)
            print('System exit (see logs)')
            sys.exit()

        mycursor = self.mydb.cursor()
        mycursor.execute(
            f"SELECT {', '.join(column_names)} FROM `mydb`.`Product`")
        myresult = mycursor.fetchall()

        row = 0
        col = 0

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        for i in range(len(column_names)):
            worksheet.write(row, col + i, column_names[i])
        row += 1

        for ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice, UnitPriceUSD, UnitPriceEuro, Ranking in myresult:
            elems = [ProductID, DepartmentID, Category, IDSKU, ProductName,
                     Quantity, UnitPrice, UnitPriceUSD, UnitPriceEuro, Ranking]
            for i in range(len(elems)):
                worksheet.write(row, col + i, elems[i])
            row += 1
        workbook.close()
