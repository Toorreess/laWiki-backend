from bson import ObjectId
from bson.errors import InvalidId
from pymongo.mongo_client import MongoClient


class MongoDBRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri: str, database_name: str, collection_name: str):
        if not hasattr(self, "initialized"):
            self.client = MongoClient(uri)
            self.database = self.client[database_name]
            self.collection = self.database[collection_name]
            self.initialized = True

    def insert_document(self, document: dict):
        document["deleted"] = False
        return self.collection.insert_one(document)

    def find_document(self, document_id: str):
        try:
            return self.collection.find_one(
                {"_id": ObjectId(document_id), "deleted": False}
            )

        except (InvalidId, TypeError) as e:
            raise ValueError(f"Invalid ObjectId: {e}")

    def list_documents(self, query: dict = {}, limit: int = 10, skip: int = 0):
        query["deleted"] = False
        return list(self.collection.find(query).limit(limit).skip(skip))

    def update_document(self, document_id: str, updates: dict):
        try:
            return self.collection.update_one(
                filter={"_id": ObjectId(document_id)}, update={"$set": updates}
            )
        except (InvalidId, TypeError) as e:
            raise ValueError(f"Invalid ObjectId: {e}")

    def delete_document(self, document_id: str):
        try:
            return self.collection.delete_one({"_id": ObjectId(document_id)})
        except (InvalidId, TypeError) as e:
            raise ValueError(f"Invalid ObjectId: {e}")

    def close_connection(self):
        self.client.close()
