from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson import ObjectId

class Roadmap(Model):
    
    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('title', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'title': None,
            'description': None,
            'activate': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }