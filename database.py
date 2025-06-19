from peewee import *
from datetime import datetime

db = SqliteDatabase('weather_bot.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
})

class BaseModel(Model):
    class Meta:
        database = db

class History(BaseModel):
    chat_id = IntegerField()
    city = CharField()
    day = CharField()
    temp = IntegerField()
    feels_like = IntegerField()
    description = CharField()
    wind_speed = FloatField()
    date_request = DateTimeField(default=datetime.now)

def initialize_db():
    db.connect()
    db.create_tables([History], safe=True)
