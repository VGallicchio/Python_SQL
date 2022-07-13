import json

#Função para transformar TSV em JSON.
def tsv2json(data_tsv,data):
    # Guardando os headers em um array. 
    # Primeira linha contendo os headers 
    arr = []
    file = open(data_tsv, 'r')
    a = file.readline()
    
    
    # separadores.
    linhas_arquivo = [t.strip() for t in a.split('\t')]
    for line in file:
        d = {}
        for t, f in zip(linhas_arquivo, line.split('\t')):
            # Com o strip removemos as quebras do TSV.    
            # Convertendo cada linha em dicionario com os titulos como chave.
            d[t] = f.strip()
    
        # Append todos valores individuais do dictionaires em uma list
        arr.append(d)       
        # Dump para JSON.
    
    with open(data, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))

#Função de insert na Collection.
def insert(data, collection):
    with open(data) as file:
        file_data = json.load(file)
    
    #Para inserir many ou one na collection.
    if isinstance(file_data, list):
        collection.insert_many(file_data)
    else:
        collection.insert_one(file_data)

#Função para dump em JSON.
def plot_json(query, nome):
    with open(f'python-NoSql\{nome}.json', 'w') as arquivo:
        json.dump(query, arquivo, indent=4)
