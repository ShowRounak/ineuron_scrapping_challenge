import mysql.connector as conn
import logging
import scrapper

logging.basicConfig(filename="sql_operations.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")


class MySQL_operations():

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_connection(self):
        try:
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
            cursor = mydb.cursor()
            self.mydb = mydb
            self.cursor = cursor
            logging.info("Connection to DB successful")
            print("Connection to DB successful")
        except Exception as e:
            logging.error("Exception occurred", e)

    def create_table(self, table_name, columns):
        try:
            self.table_name = table_name
            self.columns = columns
            self.cursor.execute(f"CREATE TABLE {self.table_name}({self.columns})")
            self.mydb.commit()
            logging.info("table has created")
            print("Table has created")
        except Exception as e:
            logging.error("Exception occurred", e)

    def insert_data(self, values):
        try:
            self.values = values
            self.cursor.execute(f"INSERT INTO {self.database}.{self.table_name} VALUES({self.values})")
            self.mydb.commit()
            logging.info("Insertion successful")
            print("Insertion successful")
        except Exception as e:
            logging.error("Exception occurred", e)


obj = scrapper.Ineuron_Scrapping()
obj.ineuron_course_data()
obj.get_all_course_titles()
courses_info = obj.scrap_all_course()


sqlobj = MySQL_operations("localhost", "root", "password", "rikdb")
sqlobj.create_connection()
sqlobj.create_table("ineuron_courses", "COURSETITLE VARCHAR(255), DESCRIPTION LONGTEXT, LANGUAGE VARCHAR(255), PRICING INT(10)")
for i in range(len(courses_info)):
    sqlobj.insert_data("'{title}', '{description}', '{langauge}', '{price}'".format(title=courses_info[i]['TITLE'],description=courses_info[i]['DESCRIPTION'], langauge=courses_info[i]['LANGUAGE'],price=courses_info[i]['PRICE_INR']))