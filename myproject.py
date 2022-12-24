from fastapi import FastAPI
from sqlalchemy import create_engine, text, Column, String, Integer
from sqlalchemy import create_engine, text
from fastapi_pagination import Page, paginate, add_pagination
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import DatabaseConnection


def connect_to_db():

    connection_url = "mysql+pymysql://root:1234@localhost:3306/CountriesPopulation"

    try:
        engine = create_engine(url=connection_url)

        # create a session
        session = sessionmaker(bind=engine)
        conn = session()

        if session:
            return conn

    except SQLAlchemyError as se:
        print(se)

Base = declarative_base()

app = FastAPI(title="Countries Capital Population",
              debug=True)
add_pagination(app)

class Countries(Base):

    __tablename__ = "Countries"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    country = Column(String)
    iso3 = Column(String)


class CountriesOut(BaseModel):
    code:str
    country:str
    iso3:str

    class Config:
        orm_mode = True

class Population(Base):

    __tablename__ = "Population"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    value = Column(String)
    year = Column(Integer)


@app.get(path="/api/countries/all", name="Gets all countries",
response_model=Page[CountriesOut])
async def get_all_countries():
    conn = connect_to_db()
    results = conn.query(Countries).all()
    return paginate(results)
    # return {"all_countries": results}

@app.get(path="/api/population/all", name="Gets all population")
async def get_all_population():
    conn = connect_to_db()
    results = conn.query(Population).all()
    return {"all_population": results}

