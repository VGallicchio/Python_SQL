--Quantidade estoque.
SELECT c.nome_modelo, p.tipo_pacote, (c.preco::money), e.quantidade
FROM carros AS c
JOIN pacote AS p
ON p.id = c.id_pacote
JOIN estoque AS e
ON e.id_carro = c.id;

--Carro por pacote e preço
SELECT c.nome_modelo, p.tipo_pacote, (c.preco::money)
FROM carros AS c
JOIN pacote AS p
ON p.id = c.id_pacote;

--Lista de todos os componentes utilizados para cada um dos pacotes de todos os carros:
SELECT car.nome_modelo AS veiculo,  p.tipo_pacote AS pacote, c.componente AS componentes_utilizados  
FROM conteudo_pacotes AS cp
JOIN componentes AS c
ON cp.id_componente = c.id
JOIN pacote AS p
ON cp.id_pacote = p.id
JOIN carros AS car
ON car.id_pacote = p.id
ORDER BY 1, 2;

--Pacote específico, lista de todos os componentes e sub-componentes cadastrados:
WITH t1 AS(
	SELECT c.componente AS nome_componente, sc.name AS nome_subcomponente
	FROM linha_montagem AS l
	JOIN componentes AS c
	ON l.id_componente = c.id 
	JOIN sub_componentes AS sc
	ON l.id_subcomponente = sc.id
	WHERE c.componente LIKE 'Central de Multimidia'),
t2 AS(
SELECT p.tipo_pacote AS pacote, c.componente AS nome_componente
	FROM pacote AS p
	JOIN conteudo_pacotes AS cp
	ON cp.id_pacote = p.id
	JOIN componentes AS c
	ON cp.id_componente = c.id
	WHERE c.componente LIKE 'Central de Multimidia')
SELECT t2.pacote, t1.nome_componente, t1.nome_subcomponente
FROM t1
JOIN t2
ON t1.nome_componente = t2.nome_componente;
