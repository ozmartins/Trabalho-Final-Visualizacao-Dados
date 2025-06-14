/*
DROP TABLE cbf.jogo CASCADE;
DROP TABLE cbf.clube CASCADE;
DROP TABLE cbf.atleta CASCADE;
DROP TABLE cbf.alteracao CASCADE;
DROP TABLE cbf.eventos CASCADE;
DROP TABLE cbf.escalacao CASCADE;
DROP TABLE cbf.campeonato CASCADE;
DROP TABLE cbf.documento CASCADE;
DROP TABLE cbf.arbitro CASCADE;
DROP TABLE cbf.penalidade CASCADE;
DROP TABLE cbf.estadio CASCADE;
DROP TABLE cbf.cidade CASCADE;
DROP TABLE cbf.equipe_arbitragem CASCADE;
*/

CREATE TABLE cbf.jogo
(
    id_jogo int PRIMARY KEY,
    num_jogo int,
    rodada int,
    grupo varchar(100),
    data date,
    hora timestamp,
    qtd_alteracoes_jogo int,
    id_campeonato int,
    id_estadio int
);

CREATE TABLE cbf.clube
(
    id_clube int PRIMARY KEY,
    nome varchar(100),
    url_escudo varchar(500)  
);

CREATE TABLE cbf.atleta
(
    id_atleta int PRIMARY KEY,
    nome varchar(100),
    apelido varchar(100),
    foto varchar(500)
);

CREATE TABLE cbf.alteracao
(
    codigo_jogador_saiu int,
    codigo_jogador_entrou int,
    tempo_jogo timestamp,
    tempo_subs varchar(3),
    tempo_acrescimo timestamp,
    id_jogo int,
    id_clube int,
    id_alteracao serial PRIMARY KEY
);

CREATE TABLE cbf.eventos
(    
	gols int,
    penaltis int,
    id_jogo int,
    id_clube int,
    PRIMARY KEY (id_jogo, id_clube)
);

CREATE TABLE cbf.escalacao
(
    numero_camisa int,
    reserva bool,
    goleiro bool,
    entrou_jogando bool,
    id_atleta int,
    id_clube int,
    id_jogo int,
    id_escalacao serial PRIMARY KEY,
	UNIQUE (id_atleta, id_clube, id_jogo)
);

CREATE TABLE cbf.campeonato
(
    id_campeonato serial PRIMARY KEY,
    nome varchar(100) UNIQUE
);

CREATE TABLE cbf.documento
(
    id_documento serial PRIMARY KEY,
    url varchar(500),
    title varchar(100),
    id_jogo int
);

CREATE TABLE cbf.arbitro
(
    id_arbitro int PRIMARY KEY,
    nome varchar(100),
    uf varchar(2),
    categoria varchar(10)
);

CREATE TABLE cbf.penalidade
(
    id_penalidade int PRIMARY KEY,
    tipo varchar(100),
    resultado varchar(100),
    tempo_jogo varchar(3),
    minutos timestamp,
    id_escalacao int	
);

CREATE TABLE cbf.estadio
(
    id_estadio serial PRIMARY KEY,
    nome varchar(100) UNIQUE,
    id_cidade int
);

CREATE TABLE cbf.cidade
(
    id_cidade serial PRIMARY KEY,
    nome varchar(100) UNIQUE,
    uf varchar(2)
);

CREATE TABLE cbf.equipe_arbitragem
(
    id_arbitro int,
    id_jogo int,
    funcao varchar(100),
    PRIMARY KEY (id_arbitro, id_jogo)
);

ALTER TABLE cbf.documento ADD CONSTRAINT fk_documento_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo);
	
ALTER TABLE cbf.estadio ADD CONSTRAINT fk_estadio_cidade
    FOREIGN KEY (id_estadio)
    REFERENCES cbf.estadio (id_estadio);
	
ALTER TABLE cbf.eventos ADD CONSTRAINT fk_eventos_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo);
	
ALTER TABLE cbf.eventos ADD CONSTRAINT fk_eventos_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube);
	
ALTER TABLE cbf.equipe_arbitragem ADD CONSTRAINT fk_equipe_arbitragem_arbitro
    FOREIGN KEY (id_arbitro)
    REFERENCES cbf.arbitro (id_arbitro);
	
ALTER TABLE cbf.equipe_arbitragem ADD CONSTRAINT fk_equipe_arbitragem_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo);
	
ALTER TABLE cbf.penalidade ADD CONSTRAINT fk_penalidade_escalacao
    FOREIGN KEY (id_escalacao)
    REFERENCES cbf.escalacao (id_escalacao);
	
ALTER TABLE cbf.alteracao ADD CONSTRAINT fk_alteracao_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo);
	
ALTER TABLE cbf.alteracao ADD CONSTRAINT fk_alteracao_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube);
	
ALTER TABLE cbf.jogo ADD CONSTRAINT fk_jogo_campeonato
    FOREIGN KEY (id_campeonato)
    REFERENCES cbf.campeonato (id_campeonato);
	
ALTER TABLE cbf.jogo ADD CONSTRAINT fk_jogo_estadio
    FOREIGN KEY (id_estadio)
    REFERENCES cbf.estadio (id_estadio);
	
ALTER TABLE cbf.escalacao ADD CONSTRAINT fk_escalacao_atleta
    FOREIGN KEY (id_atleta)
    REFERENCES cbf.atleta (id_atleta);
	
ALTER TABLE cbf.escalacao ADD CONSTRAINT fk_escalacao_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube);
	
ALTER TABLE cbf.escalacao ADD CONSTRAINT fk_escalacao_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo);