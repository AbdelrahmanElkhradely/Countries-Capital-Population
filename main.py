from flask_restful import Resource, Api, reqparse
from flask import Flask,request
import urllib.request, json
import requests
import DatabaseConnection
app = Flask(__name__)
api = Api(app)


@app.route("/population")
def get_population():
    url = "https://countriesnow.space/api/v0.1/countries/population"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data


@app.route("/pokemon")
def get_pokemon():
    # params={'limit' : '100000',  'offset':'0'}
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    params={'limit' : limit,  'offset':offset}
    url = "https://pokeapi.co/api/v2/pokemon"
    response = requests.get(url,params=params)
    data = response.json()
    print (data['count'])
    return {"pokemon": data}

@app.route("/movie")
def get_movie():
    url = "https://api.themoviedb.org/3/movie/popular?api_key=18a017b1725a276ac9a9838ec5345147"

    response = urllib.request.urlopen(url)
    data = response.read()
    jsondata = json.loads(data)

    movie_json = []

    for movie in jsondata["results"]:
        movie = {
            "title": movie["title"],
            "overview": movie["overview"],
        }

        movie_json.append(movie)
    return {"movie title": movie_json}


if __name__ == '__main__':
    DatabaseConnection.Create_Countris_Table()
    # app.run()  # run our Flask app