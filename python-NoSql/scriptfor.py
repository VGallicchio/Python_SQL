from pymongo import MongoClient

#Conexão com o Banco.
cliente = MongoClient('localhost',27017)
banco = cliente.database_players
jogadores = banco.players_collection
arquivo = 'python-NoSql/PlayerWithSalarySeason-211004-100110.tsv'
arquivo = (row for row in open(arquivo))
#Strip para linhas.
linhas_arquivo = (s.rstrip().split('\t') for s in arquivo)

#Gerando as colunas, e setando o _id.
cols = next(linhas_arquivo)
cols[1]='_id'

#Criando o dicionário a partir das colunas.
dicionario = (dict(zip(cols, dados)) for dados in linhas_arquivo)

#Criando listas para receber os parametros do dicionário.
lista=[]
dici = list(dicionario)
lista_dici=[]

#Função para agrupar e dar append.
def agrupador1(lista,lista_dici,dicionario):
    for j in dicionario:
        if j['_id'] in lista:
            colunas = [cols[2],cols[8],cols[9],cols[10],cols[11],cols[12]]
            for k in lista_dici:
                #for l in k:
                if (j['_id'])==(k['_id']):
                    escolhido =k
            i=colunas[4]
            if isinstance(escolhido[i],list)==True:
                escolhido1 = escolhido
                dici_velho1 = j
                dici_novo1 = escolhido1#problema com o uso do escolhido
                dici_novo1[i].append(dici_velho1[i])#falta adicionar mais uma vez 
                #print(dici_novo[i])
                lista_dici.remove(escolhido1)
                lista_dici.append(dici_novo1)
        else:
            lista.append(j['_id'])
            if 'PLAYER_SALARY_SEASON' in j:
                listinha =[]
                listinha.append(j['PLAYER_SALARY_SEASON'])
                j['PLAYER_SALARY_SEASON']=listinha
                lista_dici.append(j)
            else:
                lista_dici.append(j)
    return lista_dici


def agrupador2(lista,lista_dici,dicionario):
    for j in dicionario:# eu ja tenho que colocar como lista diretamente na lista_dici
        if j['_id'] in lista:
            
            colunas = [cols[2],cols[8],cols[9],cols[10],cols[11],cols[12]]
            for k in lista_dici:
                #for l in k:
                if (j['_id'])==(k['_id']):
                    escolhido =k
            i=colunas[5]
            if isinstance(escolhido[i],list)==True:
                escolhido1 = escolhido
                dici_velho1 = j
                dici_novo1 = escolhido1#problema com o uso do escolhido
                dici_novo1[i].append(dici_velho1[i])#falta adicionar mais uma vez 
                #print(dici_novo[i])
                lista_dici.remove(escolhido1)
                lista_dici.append(dici_novo1)          
        else:
            lista.append(j['_id'])
            if 'PLAYER_SALARY_AMOUNT' in j:
                listinha =[]
                listinha.append(j['PLAYER_SALARY_AMOUNT'])
                j['PLAYER_SALARY_AMOUNT']=listinha
                lista_dici.append(j)
            else:
                lista_dici.append(j)
    return lista_dici


#este código só está retornando  primeiro valor que aparece
agrupador1(lista,lista_dici,dici)
#print(dici)
lista_final = []
lista_dici_final = []

# esta entrnado aqui apenas o que sai do lista_dici
# o que sai do lista_dici possui apenas um valor de player_salary_amount
agrupador2(lista_final,lista_dici_final,dici)
#print(lista_dici_final)
def filtro(i1,j1):
    for i in i1:
        for j in j1:
            if i['_id']==j['_id']:
                if 'PLAYER_SALARY_AMOUNT' in i:
                    i['PLAYER_SALARY_AMOUNT'] = j['PLAYER_SALARY_AMOUNT']
    return(i)
            
filtro(lista_dici,lista_dici_final)
print(lista_dici)

jogadores.insert_many(lista_dici)
