from functions import *
from pymongo import MongoClient
from pymongo.collation import Collation

#Conectando com mongo, criando db e collection.
client = MongoClient('localhost', 27017)
database = client['Players_Database']
#Criando collection para a raw_data
raw_collection = database.create_collection('raw_data',
                                  collation=Collation(locale='en_US', numericOrdering=True))
#Criando collection para dataset filtrado.
players_collection = database.create_collection('jogadores_id',
                                  collation=Collation(locale='en_US', numericOrdering=True))


#Dataset para importar.
data_tsv = 'python-NoSql/PlayerWithSalarySeason-211004-100110.tsv'

#Transformando dataset em json
data = 'python-NoSql/players_ss.json'
tsv2json(data_tsv, data)

#Inserindo dataset na raw_collection
insert(data, raw_collection)

#Implementando Query para filtrar dados e posteriormente inserir na collection definitiva.
t = database.raw_data.aggregate([
    
    { "$group": {
        "_id": {
            "addr": "$ID",
            "ROW": "$ROW",
            "ACTIVE": "$ACTIVE",
            "NAME": "$NAME",
            "COUNTRY": "$COUNTRY", 
            "HEIGHT": "$HEIGHT", 
            "WEIGHT": "$WEIGHT",
            "POSITION": "$POSITION", 
            "TEAM_ID": "$TEAM_ID",
            "TEAM_CITY": "$TEAM_CITY", 
            "TEAM_STATE": "$TEAM_STATE",
            "PLAYER_SEASON": "$PLAYER_SALARY_SEASON",
            "PLAYER_SALARY": "$PLAYER_SALARY_AMOUNT"
        }
    }},
   
    { "$group": {
        "_id": "$_id.addr",
        "ROW": {"$first": "$_id.ROW"},
        "ACTIVE": {"$first": "$_id.ACTIVE"},
        "NAME": {"$first": "$_id.NAME"},
        "COUNTRY": {"$first": "$_id.COUNTRY"},
        "HEIGHT": {"$first": "$_id.HEIGHT"}, 
        "WEIGHT": {"$first": "$_id.WEIGHT"},
        "POSITION": {"$first": "$_id.POSITION"}, 
        "TEAM_ID": {"$first": "$_id.TEAM_ID"},
        "TEAM_CITY": {"$first": "$_id.TEAM_CITY"}, 
        "TEAM_STATE": {"$first": "$_id.TEAM_STATE"},
        "PLAYER_SALARY_SEASON": { 
            "$push": { 
                "PLAYER_SEASON": "$_id.PLAYER_SEASON"
            },
        },
        "PLAYER_SALARY_AMOUNT": { 
            "$push": { 
                "PLAYER_SALARY": "$_id.PLAYER_SALARY"
            },
        }
    }},
    {"$sort": {"ROW": 1}}
])
#Transformando o resultado da query em lista para plotar em json.
ltc = list(t)
#Plotando com a função.
plot_json(ltc, 'Players_Dataset')
data = 'python-NoSql/Players_Dataset.json'
#Inserindo Dataset definitivo.
insert(data, players_collection)
print('Dados Exportados com Sucesso')
