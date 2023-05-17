import re                     # Imports datetime library
import pymongo
from pymongo import MongoClient
import requests
from requests.auth import HTTPBasicAuth
import base64
import os
import time
from statistics import mean
import sqlite3

uri = '---'

client = MongoClient(uri) 

#client.list_database_names()

db = client.NBApoints

col = db["NBAtest"]


URL = "https://www.googleapis.com/customsearch/v1" 

total_points = {}


def fetch_points_from_google_search(player_name):

    key = '---'
    cx = '---'
    q = 'how many points did ' + player_name + ' score'
    fields = "items(snippet)"
    PARAMS = {
          'key': key,
          'cx': cx,
          'q': q
      }
    r = requests.get(url = 'https://www.googleapis.com/customsearch/v1', params = PARAMS, timeout=200)

    data = r.json()  
    try:
        search_slug = data['items'][0]['snippet']
        print('search_slug:' + search_slug)
        found = re.findall(r'(\w+\s+\w+)\s*-\s*(\d+)', search_slug)
        player_name, points = found[0]
        return {'player_name': player_name, 'points': float(points)}
    except Exception as e:
        return None 
    #print('Google search query:', q)

'''def fetch_points_for_all_players():
  query = {}
  documents = col.find(query)
  for document in documents:
        player_name = document['player_name']
        print('Fetching points for', player_name)
        points = fetch_points_from_google_search(player_name)
        if points:
            col.update_one({'_id': document['_id']}, {'$set': {'points': points['points']}})
        else:
            print('Failed to fetch points for', player_name)'''
          
def insert_points_to_database(point_slug):
  for player_name, points in total_points.items():
        col.update_many({'player_name': player_name}, {'$set': {'points': points}})
def lambda_handler(event, context):
    # Call the insert_points_to_database function for each player.
    query = {}
    documents = col.find(query)
    for document in documents:
        player_name = document['player_name']
        print(player_name)
        points = fetch_points_from_google_search(player_name)
        if points is not None:
            print(points)
            total_points[player_name] = points['points']
    print(total_points)
    insert_points_to_database({})
    
