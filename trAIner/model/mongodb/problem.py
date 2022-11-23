from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson import ObjectId
from controller.util import get_tier


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


    def update_problem(self, pro_id: str, document: dict):
        """문제 수정"""
        self.col.update_one(
            {'problemId': pro_id},
            {
                '$set': {
                    **document,
                    'updated_at': datetime.now()
                }
            }
        )


    def get_all_problems(self):
        """모든 문제(핫 문제) 반환"""
        return list(self.col.find(
            {'isHotProblem': True},
            {
                'problemId': 1,
                'problemNumber': 1,
                'level': 1
            }
        ))

    
    def get_random_problems(self, size: int):
        """랜덤하게 문제 반환"""
        return list(self.col.aggregate(
            [
                {
                    "$match": {'isHotProblem': True}
                },
                {"$sample": {"size": size}},
                {
                    "$project": {
                        "problemId": 1,
                        "problemNumber": 1,
                        "level": 1
                    }
                }
            ]
        ))
        

    def get_problem_info(self, pro_id: str):
        """문제 정보 반환"""
        return self.col.find_one(
            {
                'problemId': pro_id,
                'isHotProblem': True
            },
            {
                'problemId': 1,
                'titleKo': 1,
                'level': 1,
                'tags': 1,
                'correctPeople': 1,
                'timeLimit': 1,
                'memoryLimit': 1,
                'description': 1,
                'input': 1,
                'output': 1,
                'example': 1,
                'limit': 1,
                'note': 1,
                'problemNumber': 1
            }
        )
    
    def get_problem_info_many(self, pro_ids: list):
        """문제 정보 여러개 반환"""
        return list(self.col.find(
            {'problemId': {"$in": pro_ids}},
            {
                'problemId': 1,
                'titleKo': 1,
                'level': 1,
                'tags': 1,
                'correctPeople': 1,
                'timeLimit': 1,
                'memoryLimit': 1,
                'description': 1,
                'input': 1,
                'output': 1,
                'example': 1,
                'limit': 1,
                'note': 1,
                'problemNumber': 1
            }
        ))

    
    def get_problem_info_with_numbers(self, pro_numbers: list):
        """문제 번호를 이용한 문제 정보 반환"""
        return list(self.col.find(
            {'problemNumber': {'$in': pro_numbers}},
            {
                'problemId': 1,
                'titleKo': 1,
                'level': 1,
                'tags': 1,
                'correctPeople': 1,
                'timeLimit': 1,
                'memoryLimit': 1,
                'description': 1,
                'input': 1,
                'output': 1,
                'example': 1,
                'limit': 1,
                'note': 1,
                'problemNumber': 1
            }
        ))
    

    def get_problem_number(self, pro_id: str):
        """문제 번호 반환"""
        return self.col.find_one(
            {'problemId': pro_id},
            {'problemNumber': 1}
        )
    

    def get_problem_number_many(self, pro_ids: list):
        """문제 번호 리스트 반환"""
        return list(self.col.find(
            {'problemId': {'$in': pro_ids}},
            {'problemNumber': 1}
        ))

    
    def get_problem_number_by_tier(self, tier: str):
        """난이도별 문제 리스트 반환"""
        levels = get_tier(tier)
        return list(self.col.find(
            {
                'isHotProblem': True,
                'level': {'$in': levels}
            },
            {'problemNumber': 1}
        ))