import psycopg2 as db

#Classe de configuração para o banco.
class Config:
    def __init__(self):
        #recebe os dados de conexão do bdd.
        self.config = {
            "postgres":{
                "user": "postgres",
                "password": "postgres123",
                "host": "127.0.0.1",
                "port": "5432",
                "database": "players_salary"
                }
        }

#recebe as configurações para conectar ao banco.        
class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        #** Desempacotar para pegar a chave. 
        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Erro na conexão", e)
            exit(1)

#Métodos para instruções SQL:
    #Retorna o proprio objeto da classe, para conexão.
    def __enter__(self):
        return self
    
    #Para sair e fechar conexão, utilizando exc (com commit).
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()
    

    @property
    def connection(self):
        return self.conn
    
    
    @property
    def cursor(self):
        return self.cur
        
    
    def commit(self):
        self.connection.commit()
        
        
    #Para dar return em determinado registro, para as instruções SQL.
    def fetchall(self):
        return self.cursor.fetchall()
        
    
    #Para receber a instrução SQL.
    def execute(self, sql, params=None):
        #Se a instrução tiver parametros ele passa se não passa uma tupla vazia.
        self.cursor.execute(sql, params or ())
    
    
    #Para receber a query SQL.
    def query(self, sql, params=None):
        #Se a instrução tiver parametros ele passa se não passa uma tupla vazia.
        self.cursor.execute(sql, params or ())
        #Para retornar a instrução SQL.
        return self.fetchall()

#Classe para CRUDE
class Players(Connection):
    def __init__(self):
        Connection.__init__(self)


    #Função para criar tabela para inserir raw data e inserindo com copy_from.
    def insert_raw_data(self, filename):
        try:
            #Drop table caso existir
            sql_e = 'DROP TABLE IF EXISTS public.raw_table'
            #Criando a tabela para inserir a raw data
            sql = '''CREATE TABLE IF NOT EXISTS public.raw_table 
                (ROW integer,
                ID integer,
                ACTIVE boolean,
                NAME CHARACTER VARYING(80),
                COUNTRY bpchar,
                HEIGHT integer,
                WEIGHT integer,
                POSITION VARCHAR (80),
                TEAM_ID integer,
                TEAM_CITY bpchar,
                TEAM_STATE bpchar,
                PLAYER_SALARY_SEASON VARCHAR (80),
                PLAYER_SALARY_AMOUNT integer
                );
                
                CREATE TABLE IF NOT EXISTS public.teams
                (
                    id integer NOT NULL,
                    team_city character varying(80),
                    team_state character varying(80),
                    PRIMARY KEY (id)
                );

                CREATE TABLE IF NOT EXISTS public.players
                (    
                    id integer NOT NULL,
                    active boolean,
                    name character varying(80),
                    country character varying(80),
                    height integer,
                    weight integer,
                    position character varying(80),
                    team_id integer NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (team_id) REFERENCES teams (id)
                );

                CREATE TABLE IF NOT EXISTS public.salary
                (
                    season character varying(80),
                    salary_amount integer,
                    id_player integer NOT NULL,
                    FOREIGN KEY (id_player) REFERENCES players (id)
                )
                '''
            self.execute(sql_e)
            self.execute(sql)

            #Inserindo os dados do tsv com o copy_from
            self.header = next(filename)
            self.cursor.copy_from(filename, "raw_table",sep="\t",null='')
            self.commit()
            #Update para dados faltantes ficarem como nulos e não ""
            self.execute("UPDATE raw_table SET position = null WHERE position = '\"\"'")
            self.commit()
            print("Raw data inserida com sucesso")
        except Exception as e:
            print("Erro ao inserir raw_data", e)

    #Método de insert.    
    def insert(self):
        try:
            sql = """
            INSERT INTO teams(id, team_city, team_state)
            SELECT DISTINCT team_id, team_city, team_state 
            FROM raw_table;

            INSERT INTO players(id, active, name, country, height, weight, position, team_id)
            SELECT DISTINCT id, active, name, country, height, weight, position, team_id
            FROM raw_table;

            INSERT INTO salary(season, salary_amount, id_player)
            SELECT player_salary_season, player_salary_amount, id
            FROM raw_table
            WHERE player_salary_season IS NOT NULL
            AND player_salary_amount IS NOT NULL;
            """
            self.execute(sql)
            self.commit()
        except Exception as e:
            print("Erro ao inserir", e)


    #Método para deletar repetidos.
    def delete(self, id):
        try:
            #verificando se a variável existe
            sql_s = f"SELECT * FROM person WHERE id = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar"
            else:
                sql_d = f"DELETE FROM person WHERE id = {id}"
                self.execute(sql_d)
                self.commit()
                return f"Registro's repetidos {id} deletado"
        except Exception as e:
            print("Erro ao deletar", e)


if __name__ == "__main__":
    players = Players()
    #Abrindo arquivo e chamando função insert_raw_data
    arquivo = open("python-sql-jogadores/PlayerWithSalarySeason-210902-184055.tsv", 'r')
    players.insert_raw_data(arquivo)
    players.insert()

    """
    #Querys:
    #Posições mais bem paga por estado.
    print(players.query('''SELECT t.team_state, p.position, salary
		FROM (
			SELECT p.id, p.position, s.salary_amount as salary,
			ROW_NUMBER() OVER (PARTITION BY t.team_state ORDER BY s.salary_amount DESC) AS rn
			FROM players p
			JOIN salary s
			ON p.id = s.id_player
			JOIN teams t
			ON t.id = p.team_id
		)AS sub
        JOIN players p
        ON p.id = sub.id
        JOIN teams t
        ON t.id = p.team_id
        AND sub.rn = 1; '''))

    #Média, minimo e máximo de salários por altura.
    print(players.query('''
    SELECT DISTINCT p.height AS height,
        AVG(s.salary_amount) OVER salary_by_height AS avg_salary,
        MIN(s.salary_amount) OVER salary_by_height AS min_salary,
        MAX(s.salary_amount) OVER salary_by_height AS max_salary
    FROM players p
    JOIN salary s
    ON s.id_player = p.id
    WINDOW salary_by_height AS (PARTITION BY p.height ORDER BY p.height DESC)
    ORDER BY 1 DESC;
    ''')) """ 