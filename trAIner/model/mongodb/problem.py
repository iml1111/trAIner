from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson import ObjectId


class Problem(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('problemNumber', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'problemId': None,
            'titleKo': None,
            'titles': None,
            'isSolvable': None,
            'isPartial': None,
            'acceptedUserCount': None,
            'level': None,
            'votedUserCount': None,
            'sprout': None,
            'givesNoRating': None,
            'isLevelLocked': None,
            'averageTries': None,
            'official': None,
            'tags': None,
            'isHotProblem': None,
            'problemNumber': None,
            'timelimit': None,
            'memoryLimit': None,
            'submit': None,
            'correct': None,
            'correctPeople': None,
            'correctPercent': None,
            'description': None,
            'input': None,
            'output': None,
            'example': None,
            'limit': None,
            'note': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }
        

    def insert_problem(self, document):
        """문제 생성"""
        return self.col.insert_one(self.schemize(document))


    def get_problem_info(self, pro_id: ObjectId):
        """문제 정보 반환"""
        return self.col.find_one(
            {'_id': pro_id},
            {
                'titleKo': 1,
                'correctPeople': 1,
                'timeLimit': 1,
                'memoryLimit': 1,
                'description': 1,
                'input': 1,
                'output': 1,
                'example': 1,
                'limit': 1,
                'note': 1
            }
        )
    