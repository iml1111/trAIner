from datetime import datetime
from .base import Model


class MasterConfig(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return []

    @property
    def schema(self) -> dict:
        return {
            'config_type': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def get_author(self):
        return self.col.find_one(
            {'config_type': 'author'},
            {
                '_id': 1,
                'config_type': 1,
                '__author__': 1,
                'created_at': 1,
                'updated_at': 1,
            }
        )

    def insert_author(self, author: str):
        document = self.schemize({
            'config_type': 'author',
            '__author__': author
        })
        self.col.update_one(
            {'config_type':'author'},
            {'$set': document},
            upsert=True
        )

    def change_author(self, author: str):
        self.col.update_one(
            {'config_type': 'author'},
            {
                '$set': {
                    '__author__': author,
                    'updated_at': datetime.now()
                }
            }
        )

    def get_config(self, config_type: str):
        return self.col.find_one(
            {'config_type': config_type},
            {'value': 1}
        )

    def set_config(self, config_type: str, value):
        self.col.update_one(
            {'config_type': config_type},
            {
                '$set': {
                    'config_type': config_type,
                    'value': value,
                    'updated_at': datetime.now()
                }
            },
            upsert=True
        )


    def get_popular(self):
        return self.col.find_one(
            {'key': 'popular'},
            {
                '_id': 0,
                'value': 1
            }
        )

    
    def get_vulnerable(self):
        return self.col.find_one(
            {'key': 'vulnerable'},
            {
                '_id': 0,
                'value': 1
            }
        )

    
    def get_algorithm(self):
        return self.col.find_one(
            {'key': 'algorithm'},
            {
                '_id': 0,
                'value': 1
            }
        )

    
    def get_click(self):
        return self.col.find_one(
            {'key': 'click'},
            {
                '_id': 0,
                'value': 1
            }
        )