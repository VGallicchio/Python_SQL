
from mongoengine import * 
from mongoengine import connect
import os
import json
from mongoengine.fields import Document,ListField,StringField

#connect('database_players')
#connect(host="mongodb://127.0.0.1:27017/database_players")

class Players(Document):
    _id = StringField()
    ROW = StringField()
    ACTIVE = StringField()
    NAME = StringField()
    COUNTRY = StringField()
    HEIGHT = StringField()
    WEIGHT = StringField()
    POSITION = StringField()
    TEAM_ID = StringField()
    TEAM_CITY = StringField()
    TEAM_STATE = StringField()
    PLAYER_SALARY_SEASON = ListField()
    PLAYER_SALARY_AMOUNT = ListField()
    
    meta = {'collection': 'jogadores_id'}

    def plot_json(query, nome):
        if not os.path.exists("python-NoSql-Querys/Mongoengine-Querys"):
            try:
                os.makedirs("python-NoSql-Querys/Mongoengine-Querys")
            except Exception as e:
                print(e)
                raise
        with open(os.path.join('python-NoSql-Querys/Mongoengine-Querys', f'{nome}.json'), 'w') as arquivo:
            json.dump(query, arquivo, indent=4)
    
        return print(f'Query {nome} exportada com sucesso')

