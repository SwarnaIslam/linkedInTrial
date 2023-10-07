from pymongo import MongoClient
from dotenv import dotenv_values

config=dotenv_values('env')

conn = MongoClient("mongodb://mongodb:27017")
post_db=conn['post-service']