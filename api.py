from pymongo import MongoClient
import pandas as pd
from datetime import datetime 

def init_db():
    cluster = 'mongodb://localhost:27017/'
    try:
        client = MongoClient(cluster)
    except:
        print('Could not connect to MongoDB')
    try:
        db = client['Boulevard_Airlines']
    except Exception as e:
        print(e)
    db = client.Boulevard_Airlines
    return db

# Build Metojet routes
def metro_jet_create(airport):
    db = init_db()
    collection = db.metrojet

#get a single route
def get_route(ap1,ap2):
    db = init_db()
    collection = db.route_table
    df = pd.DataFrame(list(collection.find({'Origin':ap1, 'Destination':ap2})))
    return df
#get all airports
def get_all_airports():
    db = init_db()
    collection = db.airports
    AIRPORTS_DF = pd.DataFrame(list(collection.find()))
    return AIRPORTS_DF

#delete a route from the database
def delete_route(id):
    db = init_db()
    collection = db.route_table
    query = {'_id':id}
    result = collection.delete_one(query)
    return result

# Gather aircraft
def get_ac_data(aircraft):
    db = init_db()
    collection = db.aircraft
    df = pd.DataFrame(list(collection.find({'ICAO Code':aircraft})))
    return df

def get_routes_from_new_table(ap1,ap2):
    db = init_db()
    collection = db.new_route_table
    query = {'Origin':ap1,'Destination:':ap2}
    df = pd.DataFrame(list(collection.find(query)))
    return df