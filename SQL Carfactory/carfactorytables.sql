BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS public.carros
(
    id integer NOT NULL,
    nome_modelo character varying(80) NOT NULL,
    ano_modelo date,
	id_pacote integer,
	preco numeric NOT NULL, 
    PRIMARY KEY (id),
	FOREIGN KEY (id_pacote) REFERENCES pacote (id)
);
-- Insert Tabela Carros:
INSERT INTO carros VALUES (1,'Hb20','2021-01-01', 101, 59290.00);
INSERT INTO carros VALUES (2,'Hb20','2021-01-01', 102, 69190.00);
INSERT INTO carros VALUES (3,'Hb20','2021-01-01', 103, 79190.00);
INSERT INTO carros VALUES (4,'ix35','2020-12-31', 101, 113990.00);
INSERT INTO carros VALUES (5,'ix35','2020-12-31', 102, 133990.00);
INSERT INTO carros VALUES (6,'ix35','2020-12-31', 103, 153990.00);
INSERT INTO carros VALUES (7,'Azera','2021-01-01', 101, 269900.00);
INSERT INTO carros VALUES (8,'Azera','2021-01-01', 102, 289900.00);
INSERT INTO carros VALUES (9,'Azera','2021-01-01', 103, 300000.00);

CREATE TABLE IF NOT EXISTS public.pacote
(
    id integer NOT NULL,
    tipo_pacote character varying(80) NOT NULL,
    PRIMARY KEY (id)
);
--Insert Tabela Pacote:
INSERT INTO pacote VALUES (101,'Basic');
INSERT INTO pacote VALUES (102,'Comfortline');
INSERT INTO pacote VALUES (103,'Highline');

CREATE TABLE IF NOT EXISTS public.componentes
(
    id integer NOT NULL,
    componente character varying(80) NOT NULL,
	qtd_componente integer NOT NULL,
    PRIMARY KEY (id)
);
-- Insert Tabela Componentes:
INSERT INTO componentes VALUES (301,'AirBag',100);
INSERT INTO componentes VALUES (302,'Direção Hidraulica',150);
INSERT INTO componentes VALUES (303,'Trava Elétrica',250);
INSERT INTO componentes VALUES (304,'Ar Condicionado',50);
INSERT INTO componentes VALUES (305,'Direção Elétrica',150);
INSERT INTO componentes VALUES (306,'Vidros Elétricos',300);
INSERT INTO componentes VALUES (307,'Retrovisor Elétricos',250);
INSERT INTO componentes VALUES (308,'Central de Multimidia',100);
INSERT INTO componentes VALUES (309,'Sensor Estacionamento',250);

CREATE TABLE IF NOT EXISTS public.sub_componentes
(
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    qtd_subcomponentes integer NOT NULL,
    PRIMARY KEY (id)
);
--Insert Tabela sub_componentes
INSERT INTO sub_componentes VALUES (401,'Vidro',500);
INSERT INTO sub_componentes VALUES (402,'Componentes Elétricos',800);
INSERT INTO sub_componentes VALUES (403,'Tela LCD',500);
INSERT INTO sub_componentes VALUES (404,'Processador',500);

CREATE TABLE IF NOT EXISTS public.linha_montagem
(
    id_componente integer NOT NULL,
	id_subcomponente integer NOT NULL,
	FOREIGN KEY (id_componente) REFERENCES componentes (id),
	FOREIGN KEY (id_subcomponente) REFERENCES sub_componentes (id)
);
INSERT INTO linha_montagem VALUES (301, 402);
INSERT INTO linha_montagem VALUES (306, 401);
INSERT INTO linha_montagem VALUES (306, 402);
INSERT INTO linha_montagem VALUES (307, 401);
INSERT INTO linha_montagem VALUES (307, 402);
INSERT INTO linha_montagem VALUES (308, 403);
INSERT INTO linha_montagem VALUES (308, 404);
INSERT INTO linha_montagem VALUES (308, 402);

CREATE TABLE IF NOT EXISTS public.conteudo_pacotes
(
    id_pacote integer NOT NULL,
	id_componente integer NOT NULL,
	FOREIGN KEY (id_pacote) REFERENCES pacote (id),
	FOREIGN KEY (id_componente) REFERENCES componentes (id)
);
--Insert Tabela conteudo_pacotes
INSERT INTO conteudo_pacotes VALUES (101, 302);
INSERT INTO conteudo_pacotes VALUES (101, 303);
INSERT INTO conteudo_pacotes VALUES (101, 306);
INSERT INTO conteudo_pacotes VALUES (102, 302);
INSERT INTO conteudo_pacotes VALUES (102, 303);
INSERT INTO conteudo_pacotes VALUES (102, 304);
INSERT INTO conteudo_pacotes VALUES (102, 306);
INSERT INTO conteudo_pacotes VALUES (102, 307);
INSERT INTO conteudo_pacotes VALUES (103, 301);
INSERT INTO conteudo_pacotes VALUES (103, 302);
INSERT INTO conteudo_pacotes VALUES (103, 303);
INSERT INTO conteudo_pacotes VALUES (103, 304);
INSERT INTO conteudo_pacotes VALUES (103, 305);
INSERT INTO conteudo_pacotes VALUES (103, 306);
INSERT INTO conteudo_pacotes VALUES (103, 307);
INSERT INTO conteudo_pacotes VALUES (103, 308);
INSERT INTO conteudo_pacotes VALUES (103, 309);

CREATE TABLE IF NOT EXISTS public.fornecedores
(
    id integer NOT NULL,
    nome_fornecedor character varying(80) NOT NULL,
	id_componente integer,
	id_subcomponente integer,
    PRIMARY KEY (id),
	FOREIGN KEY (id_componente) REFERENCES componentes (id),
	FOREIGN KEY (id_subcomponente) REFERENCES sub_componentes (id)
);
-- Inserts Tabela Fornecedor:
INSERT INTO fornecedores VALUES (201,'Protecta', 301);
INSERT INTO fornecedores VALUES (202,'Tury Eletro',null,402);
INSERT INTO fornecedores VALUES (203,'Eletro Acessorios',null,402);
INSERT INTO fornecedores VALUES (204,'ArMais',304);
INSERT INTO fornecedores VALUES (205,'AutoGlass',null,401);
INSERT INTO fornecedores VALUES (206,'LCD Plus',null,403);
INSERT INTO fornecedores VALUES (207,'AllCar',303);
INSERT INTO fornecedores VALUES (208,'ProcessaCar',null,404);

CREATE TABLE IF NOT EXISTS public.estoque
(
    quantidade integer NOT NULL,
	id_carro integer NOT NULL,
	FOREIGN KEY (id_carro) REFERENCES carros (id)
);
-- Inserts Tabela Estoque:
INSERT INTO estoque VALUES (10, 1);
INSERT INTO estoque VALUES (5, 2);
INSERT INTO estoque VALUES (2, 3);
INSERT INTO estoque VALUES (15, 4);
INSERT INTO estoque VALUES (2, 5);
INSERT INTO estoque VALUES (3, 6);
INSERT INTO estoque VALUES (5, 7);
INSERT INTO estoque VALUES (2, 8);
INSERT INTO estoque VALUES (3, 9);
COMMIT;