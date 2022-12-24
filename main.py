from flask_restful import Resource, Api, reqparse
from flask import Flask,request
import urllib.request, json
import requests
import DatabaseConnection
app = Flask(__name__)
api = Api(app)
import threading

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
    DatabaseConnection.Create_Countris_Table()
    return {"message": "Accepted"}, 202
@app.route("/createpopulationtable")
def Create_Population_Table():
    DatabaseConnection.Create_Population_Table()
    return {"message": "Accepted"}, 202

@app.route("/syncCountries")
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


# @app.route("/pokemon")
# def get_pokemon():
#     # params={'limit' : '100000',  'offset':'0'}
#     limit = request.args.get('limit')
#     offset = request.args.get('offset')
#     params={'limit' : limit,  'offset':offset}
#     url = "https://pokeapi.co/api/v2/pokemon"
#     response = requests.get(url,params=params)
#     data = response.json()
#     print (data['count'])
#     return {"pokemon": data}
#
# @app.route("/movie")
# def get_movie():
#     url = "https://api.themoviedb.org/3/movie/popular?api_key=18a017b1725a276ac9a9838ec5345147"
#
#     response = urllib.request.urlopen(url)
#     data = response.read()
#     jsondata = json.loads(data)
#
#     movie_json = []
#
#     for movie in jsondata["results"]:
#         movie = {
#             "title": movie["title"],
#             "overview": movie["overview"],
#         }
#
#         movie_json.append(movie)
#     return {"movie title": movie_json}


if __name__ == '__main__':
    # DatabaseConnection.Create_Population_Table()
    app.run()  # run our Flask app