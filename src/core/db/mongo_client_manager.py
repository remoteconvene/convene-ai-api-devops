from pymongo import MongoClient

from src.core.config.settings import settings


class MongoClientManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.mongo_client = None

    def initialize_client(self):
        try:
            self.mongo_client = MongoClient(self.connection_string)
            self.mongo_client.server_info()
            return True  # Connection successful
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False  # Connection failed

    def is_connected(self):
        try:
            self.mongo_client.server_info()
            return True  # Connection exist
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False  # Connection not exists

    def close_client(self):
        if self.mongo_client:
            self.mongo_client.close()
            print("MongoDB client closed.")


mongo_client_manager = MongoClientManager(settings.MONGODB_URL)
