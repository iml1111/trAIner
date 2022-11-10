from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model


class User(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('id', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'id': None,
            'password': None,
            'name': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def insert_user(self, document):
        """user 생성"""
        return self.col.insert_one(self.schemize(document))

    def get_password_with_id(self, user_id: str):
        """user_id를 통한 PW 조회"""
        return self.col.find_one(
            {'id': user_id},
            {'password': 1}
        )
    
    def get_userinfo(self, user_id: str):
        """user 정보 반환"""
        return self.col.find_one(
            {'id': user_id},
            {
                'id': 1,
                'name': 1,
                'created_at': 1,
                'updated_at': 1
            }
        )
    
    