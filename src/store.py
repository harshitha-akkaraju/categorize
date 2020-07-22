import pymongo
import ssl

class Store:
    def __init__(self, host, port, username, password, app_name):
        uri = self.__prepare_connection_string(host, port, username, password, app_name)
        self.client = pymongo.MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
    
    def get_database(self, database_name):
        return self.client[database_name]
    
    def get_collection(self, database_name, collection_name):
        db = self.client[database_name]
        return db[collection_name]

    def insert_one(self, database_name, collection_name, document):
        collection = self.get_collection(database_name, collection_name)
        result = collection.insert_one(document)
        
    def insert_many(self, database_name, collection_name, documents):
        collection = self.get_collection(database_name, collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids
    
    def list_databases(self):
        return self.client.list_databases()
    
    def __prepare_connection_string(self, host, port, username, password, app_name, ssl_enabled="true"):
        connection_string = "mongodb://{0}:{1}@{2}:{3}/?ssl={4}&replicaSet=globaldb&maxIdleTimeMS=120000&retrywrites=false&appName=@{5}@"
        return connection_string.format(username, password, host, port, ssl_enabled, app_name)