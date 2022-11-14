from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson import ObjectId


class User(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('userId', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'userId': None,
            'password': None,
            'name': None,
            'userNumber': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def insert_user(self, document):
        """user 생성"""
        return self.col.insert_one(self.schemize(document))
    
    def get_all_users(self):
        """모든 유저(핫 유저) 반환"""
        return list(self.col.find(
            {'isHotUser': True},
            {'userNumber': 1}
        ))

    def get_password_with_id(self, user_id: str):
        """user_id를 통한 PW 조회"""
        return self.col.find_one(
            {'userId': user_id},
            {'password': 1}
        )
    
    def get_userinfo(self, user_oid: ObjectId):
        """user 정보 반환"""
        return self.col.find_one(
            {'_id': user_oid},
            {
                'userId': 1,
                'name': 1,
                'isHotUser': 1,
                'created_at': 1,
                'updated_at': 1
            }
        )
    
    def get_userinfo_simple(self, user_oid: ObjectId):
        """간단한 user 정보 반환"""
        return self.col.find_one(
            {'_id': user_oid},
            {
                'userId': 1,
                'userNumber': 1
            }
        )
    
    