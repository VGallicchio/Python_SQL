from mongoengine_con import *

connect(host="mongodb://127.0.0.1:27017/Players_Database")

#Quais os jogadores que moram em Oregon?
"""for oregon_players in Players.objects(TEAM_STATE='Oregon'):
    print('Estado: ', oregon_players.TEAM_STATE, ' Nome: ', oregon_players.NAME)
"""
oregon_players = Players.objects(TEAM_STATE='Oregon')
json_data = oregon_players.to_json()
loregon = list(json.loads(json_data))
Players.plot_json(loregon, 'Oregon_Players')

#Quais jogadores moram nos EUA E pesam mais que 200?
"""for us in Players.objects(COUNTRY='USA', WEIGHT__gt='200'):
    print('Peso: ', us.WEIGHT, ' Nome: ', us.NAME, ' Pais: ', us.COUNTRY)"""

us = Players.objects(COUNTRY='USA', WEIGHT__gt='200')
json_data = us.to_json()
us = list(json.loads(json_data))
Players.plot_json(us, 'EUAMore200W_players')

#Quais jogadores atuam em posição "Center" OU "Guard"?
"""for c in Players.objects(POSITION__in= ['Center','Guard']):
    print('Posição: ', c.POSITION, ' Nome: ', c.NAME)

"""
centguard = Players.objects(POSITION__in= ['Center','Guard'])
json_data = centguard.to_json()
centguard = list(json.loads(json_data))
Players.plot_json(centguard, 'Center_Guard_players')

#Lista de todos os times com seus respectivos estados (apenas uma linha por time)
"""for ts in Players.objects(TEAM_STATE__exists='TEAM_CITY').distinct(field='TEAM_CITY'):
    print('Time: ', ts)
"""
t = Players.objects().aggregate([{
    "$group":{
    "_id": {"TID": "$TEAM_ID", "Team": "$TEAM_CITY", "State": "$TEAM_STATE"}}

}])
ltc = list(t)
Players.plot_json(ltc, 'All_Teams')
