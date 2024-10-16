from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

class MongoDBManager:
    def __init__(self, db_name, collection_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        try:
            self.collection = self.db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created in database '{db_name}'.")
        except CollectionInvalid:
            self.collection = self.db[collection_name]
            print(f"Collection '{collection_name}' already exists in database '{db_name}'.")

    def append_document(self, document):
        try:
            self.collection.insert_one(document)
            print("Document inserted:", document)
        except Exception as e:
            print("Error inserting document:", e)

#For reference keep this code
# if __name__ == "__main__":
#     manager = MongoDBManager("my_database", "my_collection")
#     sample_document = {"unique_field": 1, "data": "example data"}
#     manager.append_document(sample_document)
