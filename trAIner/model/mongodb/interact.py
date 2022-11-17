from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson import ObjectId

class Interact(Model):
    
    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('userId', ASCENDING)]),
            IndexModel([('problemId', ASCENDING)]),
            IndexModel([('created_at', DESCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'submitId': None,
            'userId': None,
            'problemId': None,
            'result': None,
            'memory': None,
            'time': None,
            'language': None,
            'codeLength': None,
            'timestamp': None,
            '__version__': self.VERSION,
        }
    
    #HotInteract의 userId 와 problemId는 원래 데이터의 userNumber, problemNumber임.
    
    def get_interact_cnt(self):
        """interact 데이터 반환"""
        return list(self.col.aggregate([
            {
                "$group": {
                    "_id": "$problemId",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ]))
    
    
    def get_all_interact(self):
        return list(self.col.find())
    

    def get_interact_v2(self, pro_ids: list):
        return list(self.col.find({
            "problemId": {"$in": pro_ids}
        }))