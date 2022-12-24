import mysql.connector
from mysql.connector import Error

def Test_connection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
def Create_Countris_Table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        mySql_create_query = """CREATE TABLE IF NOT EXISTS Countries (
                                id INT auto_increment,
                                code VARCHAR(5),
                                country VARCHAR(255),
                                iso3 VARCHAR(5),
                                primary key (id)
                                )"""

        cursor = connection.cursor()
        cursor.execute(mySql_create_query)
        connection.commit()
        print(cursor.rowcount, "table created successfully into datebase")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to create table{}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")