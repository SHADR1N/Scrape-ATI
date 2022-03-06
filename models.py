import peewee


db = peewee.SqliteDatabase('database.db')
class BaseModel(peewee.Model):
    class Meta:
        database = db


class Users(BaseModel):
    USERID = peewee.IntegerField( unique = True)
    Selects = peewee.TextField(default = '')

    @classmethod
    def get_row(cls, USERID):
        return cls.get(USERID == USERID)

    @classmethod
    def row_exists(cls, USERID):
        query = cls().select().where(cls.USERID == USERID)
        return query.exists()


    @classmethod
    def creat_row(cls, USERID):
        user, created = cls.get_or_create(USERID=USERID)

        
class Search(BaseModel):
    URL = peewee.TextField(default = '')
    UID = peewee.TextField(default = '')
    name = peewee.TextField(default = '')



db.create_tables([Users])
db.create_tables([Search])
