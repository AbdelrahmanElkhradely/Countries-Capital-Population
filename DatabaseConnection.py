import mysql.connector
from mysql.connector import Error
from flask_restful import Resource, Api, reqparse
from flask import Flask,request
import requests
import time
import threading
import psycopg2


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
def Create_Countries_Table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')

        mySql_create_query = """CREATE TABLE IF NOT EXISTS Countries (
                                ID SERIAL PRIMARY KEY,
                                code VARCHAR(5),
                                country VARCHAR(255),
                                iso3 VARCHAR(5)
                                
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
def Create_Population_Table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        mySql_create_query = """CREATE TABLE IF NOT EXISTS Population (
                                ID SERIAL PRIMARY KEY,
                                code VARCHAR(5),
                                value VARCHAR(40),
                                year INT
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
def Delete_all_population():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        mySql_create_query = "DELETE from Population  "

        cursor = connection.cursor()
        cursor.execute(mySql_create_query)
        connection.commit()
        print(cursor.rowcount, "table cleared successfully into datebase")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to create table{}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
def Delete_all_countries():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        mySql_create_query = "DELETE from Countries  "

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

def Sync_Population(Population_data):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        cursor = connection.cursor()

        mySql_insert_population_query = """INSERT INTO Population (code,value,year) VALUES (%s, %s, %s) """
        Population_to_insert = []
        for temp in Population_data:
            if len(temp) == 3:
                Population_to_insert.append(temp)

        cursor.executemany(mySql_insert_population_query, Population_to_insert)

        connection.commit()

        print(cursor.rowcount, "Record inserted successfully into population table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def Sync_Countries(Countries_data):
    Countries_to_insert=[]
    for temp in Countries_data:
        if len(temp) == 3:
            Countries_to_insert.append(temp)

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        cursor = connection.cursor()

        mySql_insert_country_query = """INSERT INTO Countries (code,country,iso3)
                               VALUES (%s, %s, %s) """

        records_to_insert = Countries_data[1::]

        cursor.executemany(mySql_insert_country_query, Countries_to_insert)

        connection.commit()


        print(cursor.rowcount, "Record inserted successfully into countries table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def Sync_all_data(data):

    Delete_all_countries()
    Delete_all_population()

    Countries_data = [[]]
    Population_data = [[]]
    for c in data['data']:
        if len(c['code']) == 0:
            continue
        else:
            Countries_data.append((c['code'], c['country'], c['iso3']))
            for p in c['populationCounts']:
                Population_data.append((c['code'], p['value'], p['year']))

    Sync_Countries(Countries_data)
    Sync_Population(Population_data)

def get_country_population(countryname):
    countryname=(countryname['countryname'],)
    print(countryname)
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        mySql_create_query = """SELECT Countries.country , Population.year ,Population.value 
                             from Countries
                             left join Population 
                             on Countries.code = Population.code 
                             where country = %s"""


        cursor = connection.cursor()
        cursor.execute(mySql_create_query,countryname)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    except mysql.connector.Error as error:
        print("Failed to retrive the data {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def get_all_country_population(pagenumber):
    pagenumber=int(pagenumber['pagenumber'])
    offset=(pagenumber-1)*50
    print(pagenumber)
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='CountriesPopulation',
                                             user='root',
                                             password='1234')
        mySql_create_query = """SELECT Countries.country , Population.year ,Population.value 
                             from Countries
                             left join Population 
                             on Countries.code = Population.code 
                             LIMIT 50
                             OFFSET %s"""


        cursor = connection.cursor()
        cursor.execute(mySql_create_query,(offset,))
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    except mysql.connector.Error as error:
        print("Failed to retrive the data {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


