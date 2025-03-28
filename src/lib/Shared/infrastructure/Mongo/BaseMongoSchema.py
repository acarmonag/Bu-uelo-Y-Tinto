from datetime import datetime

from bson import ObjectId
from mongoengine import Document, DateTimeField, ObjectIdField, IntField


class BaseDocument(Document):
    meta = {"abstract": True}

    _id = ObjectIdField(primary_key=True, default=ObjectId)
    version = IntField(db_field='__v', default=0)
    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)
