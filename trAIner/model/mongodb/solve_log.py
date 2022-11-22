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
            'resultInfo': None,
            'executionTime': None,
            'code': None,
            'created_at': datetime.now(),
            '__version__': self.VERSION,
        }

    
    def insert_solve_log(self, document: dict):
        return self.col.insert_one(
            self.schemize(document)
        )
    

    def get_solve_log(self, user_id: str, skip: int, limit: int):
        """특정 유저의 풀이기록 반환"""
        return list(
            self.col.find(
                {'userId': user_id}
            ).sort('created_at', DESCENDING)
            .skip(skip)
            .limit(limit)
        )
    

    def get_latest_solve_log(self, user_id: str):
        """특정 유저가 가장 최근에 맞춘 기록 반환"""
        return list(self.col.find(
            {
                'userId': user_id,
                'result': True
            }
        ).sort('created_at', DESCENDING))
    

    def get_correct_solve_log(self, user_id: str, pro_id: str):
        """특정 유저가 해당 문제를 맞춘 기록 반환"""
        return self.col.find_one(
            {
                'userId': user_id,
                'problemId': pro_id,
                'result': True
            }
        )


    def get_latest_solve_log_by_problem_id(self, user_id: str, pro_id: str):
        """특정 문제에서 유저가 가장 최근에 제출한 기록 반환"""
        return list(self.col.find(
            {
                'userId': user_id,
                'problemId': pro_id
            }
        ).sort('created_at', DESCENDING))
