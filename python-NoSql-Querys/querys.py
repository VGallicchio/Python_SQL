import json
from pymongo import MongoClient
import os
from pprint import pprint

client = MongoClient('localhost', 27017)
database = client['Players_Database']

def plot_json(query, nome):
    if not os.path.exists("python-NoSql-Querys/Pymongo-Querys"):
        try:
            os.makedirs("python-NoSql-Querys/Pymongo-Querys")
        except Exception as e:
            print(e)
            raise
    with open(os.path.join('python-NoSql-Querys/Pymongo-Querys', f'{nome}.json'), 'w') as arquivo:
        json.dump(query, arquivo, indent=4)
   
    return print(f'Query {nome} exportada com sucesso')


#Querys

#Quais os jogadores que moram em Oregon?
#for o in database.jogadores_id.find({"TEAM_STATE": "Oregon"}):
    #pprint(o)
    
oregon_players = database.jogadores_id.find({"TEAM_STATE": "Oregon"})
loregon= list(oregon_players)
plot_json(loregon, 'Oregon_Players')

#Quais jogadores moram nos EUA E pesam mais que 200?
#for u in database.jogadores_id.find( {"COUNTRY": "USA", "WEIGHT": {"$gt": "200"}}):
    #pprint(u)
    
us = database.jogadores_id.find( {"COUNTRY": "USA", "WEIGHT": {"$gt": "200"}})
lus = list(us)
plot_json(lus, 'EUAMore200W_players')

#Quais jogadores atuam em posição "Center" OU "Guard"?
#for centguard in database.jogadores_id.find( {"$or": [ {"POSITION": "Center"}, {"POSITION": "Guard" } ]  } ):
    #pprint(centguard)

centguard = database.jogadores_id.find({"$or": [{"POSITION": "Center"}, {"POSITION": "Guard" }]})
lc = list(centguard)
plot_json(lc, 'Center_Guard_players')

#Lista de todos os times com seus respectivos estados ( apenas uma linha por time )
t = database.jogadores_id.aggregate([{
    "$group":{
    "_id": {"TID": "$TEAM_ID", "Team": "$TEAM_CITY", "State": "$TEAM_STATE"}}
}])

ltc = list(t)
plot_json(ltc, 'All_Teams')
