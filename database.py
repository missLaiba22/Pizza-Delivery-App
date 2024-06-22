from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING

client = AsyncIOMotorClient("mongodb://localhost:27017/")  


db = client["pizza_delivery"]  

users_collection = db["users"]
orders_collection = db["orders"]
pizzas_collection = db["pizzas"]

def get_database():
    return db


def close_connection():
    client.close()

