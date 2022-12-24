from flask_restful import Resource, Api, reqparse
from flask import Flask,request
import requests

import DatabaseConnection
import threading

app = Flask(__name__)
api = Api(app)


@app.route("/deleteallpopulation")
def delete_all_population():
    DatabaseConnection.Delete_all_population()
    return {"message": "Accepted"}, 202

@app.route("/deleteallcountries")
def delete_all_countries():
    DatabaseConnection.Delete_all_countries()
    return {"message": "Accepted"}, 202

@app.route("/createcountrytable")
def Create_Country_Table():
    DatabaseConnection.Create_Countries_Table()
    return {"message": "Accepted"}, 202
@app.route("/createpopulationtable")
def Create_Population_Table():
    DatabaseConnection.Create_Population_Table()
    return {"message": "Accepted"}, 202

@app.route("/syncdata")
def update_all_data():
    url = "https://countriesnow.space/api/v0.1/countries/population"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    def long_running_task(**kwargs):
        your_params = kwargs.get('data')
        DatabaseConnection.Sync_all_data(your_params)

    thread = threading.Thread(target=long_running_task, kwargs={
        'data': data})
    thread.start()
    return {"message": "Accepted"}, 202

@app.route("/getcountrypopulation")
def get_country_population():
    countryname = request.args.get('countryname')
    params={'countryname' : countryname}
    response=DatabaseConnection.get_country_population(params)
    data=[]
    for x in response:
        dict={'1-country name':x[0],'2-year':x[1], '3-Population number':x[2]}
        data.append(dict)
    # data = data.json()
    # return {"message": "Accepted"}, 202
    # # print(data)
    return data

@app.route("/getallcountriespopulation")
def get_all_country_population():

    pagenumber = request.args.get('pagenumber')
    params={'pagenumber' : pagenumber}
    response=DatabaseConnection.get_all_country_population(params)
    data=[]
    for x in response:
        dict={'1-country name':x[0],'2-year':x[1], '3-Population number':x[2]}
        data.append(dict)
    # data = data.json()
    # return {"message": "Accepted"}, 202
    # # print(data)
    return data


if __name__ == '__main__':
    # DatabaseConnection.Create_Population_Table()
    app.run()  # run our Flask app