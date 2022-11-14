from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson import ObjectId

class SolveLog(Model):
    
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
            'userId': None,
            'problemId': None,
            'result': None,
            'description': None,
            'executionTime': None,
            'code': None,
            'created_at': datetime.now(),
            '__version__': self.VERSION,
        }
    

    def get_solve_log(self, user_id: str, skip: int, limit: int):
        """특정 유저의 풀이기록 반환"""
        return list(
            self.col.find(
                {'userId': user_id}
            ).sort('created_at', DESCENDING)
            .skip(skip)
            .limit(limit)
        )