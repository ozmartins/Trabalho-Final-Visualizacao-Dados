DROP TABLE cbf.jogo CASCADE;
DROP TABLE cbf.clube CASCADE;
DROP TABLE cbf.atleta CASCADE;
DROP TABLE cbf.alteracao CASCADE;
DROP TABLE cbf.evento CASCADE;
DROP TABLE cbf.campeonato CASCADE;
DROP TABLE cbf.documento CASCADE;
DROP TABLE cbf.arbitro CASCADE;
DROP TABLE cbf.equipe_arbitragem CASCADE;
DROP TABLE cbf.penalidade CASCADE;
DROP TABLE cbf.estadio CASCADE;
DROP TABLE cbf.cidade CASCADE;
DROP TABLE cbf.escalacao CASCADE;

CREATE TABLE cbf.jogo (
    id_jogo int,
    num_jogo int,
    rodada int,
    grupo varchar(100),
    data date,
    hora timestamp,
    qtd_alteracoes_jogo int,
    id_campeonato int,
    id_estadio int,
    id_clube_mandante int,
    id_clube_visitante int
);
 
ALTER TABLE cbf.jogo ADD CONSTRAINT pk_jogo PRIMARY KEY (id_jogo);

CREATE TABLE cbf.clube (
    id_clube int,
    nome varchar(100),
    url_escudo varchar(500)
);
 
ALTER TABLE cbf.clube ADD CONSTRAINT pk_clube PRIMARY KEY (id_clube);

CREATE TABLE cbf.atleta (
    id_atleta int,
    nome varchar(100),
    apelido varchar(100),
    foto varchar(500)
);
 
ALTER TABLE cbf.atleta ADD CONSTRAINT pk_atleta PRIMARY KEY (id_atleta);

CREATE TABLE cbf.alteracao (
    id_alteracao serial,
    codigo_jogador_saiu int,
    codigo_jogador_entrou int,
    tempo_jogo timestamp,
    tempo_subs varchar(3),
    tempo_acrescimo timestamp,
    id_jogo int,
    id_clube int
);
 
ALTER TABLE cbf.alteracao ADD CONSTRAINT pk_alteracao PRIMARY KEY (id_alteracao);

CREATE TABLE cbf.evento (
    id_jogo int,
    id_clube int,
    gols int,
    penaltis int
);
 
ALTER TABLE cbf.evento ADD CONSTRAINT pk_evento PRIMARY KEY (id_clube, id_jogo);

CREATE TABLE cbf.campeonato (
    id_campeonato int,
    nome varchar(100) UNIQUE
);
 
ALTER TABLE cbf.campeonato ADD CONSTRAINT pk_campeonato PRIMARY KEY (id_campeonato);

CREATE TABLE cbf.documento (
    id_documento serial,
    url varchar(500),
    title varchar(100),
    id_jogo int
);
 
ALTER TABLE cbf.documento ADD CONSTRAINT pk_documento PRIMARY KEY (id_documento);

CREATE TABLE cbf.arbitro (
    id_arbitro int,
    nome varchar(100),
    uf varchar(2),
    categoria varchar(100)
);
 
ALTER TABLE cbf.arbitro ADD CONSTRAINT pk_arbitro PRIMARY KEY (id_arbitro);

CREATE TABLE cbf.equipe_arbitragem (
    id_arbitro int,
    id_jogo int,
    funcao varchar(100)
);
 
ALTER TABLE cbf.equipe_arbitragem ADD CONSTRAINT pk_equipe_arbitragem PRIMARY KEY (id_jogo, id_arbitro);

CREATE TABLE cbf.penalidade (
    id_penalidade int,
    tipo varchar(100),
    resultado varchar(100),
    tempo_jogo varchar(3),
    minutos timestamp,
    id_jogo int,
    id_clube int,
    id_atleta int
);
 
ALTER TABLE cbf.penalidade ADD CONSTRAINT pk_penalidade PRIMARY KEY (id_penalidade);

CREATE TABLE cbf.estadio (
    id_estadio serial,
    nome varchar(100) UNIQUE,
    id_cidade serial
);
 
ALTER TABLE cbf.estadio ADD CONSTRAINT pk_estadio PRIMARY KEY (id_estadio);

CREATE TABLE cbf.cidade (
    id_cidade serial,
    nome varchar(100) UNIQUE,
    uf varchar(2)
);
 
ALTER TABLE cbf.cidade ADD CONSTRAINT pk_cidade PRIMARY KEY (id_cidade);

CREATE TABLE cbf.escalacao (
    id_escalacao serial,
    numero_camisa int,
    reserva bool,
    goleiro bool,
    entrou_jogando bool,
    id_clube int,
    id_atleta int,
    id_jogo int
);
 
ALTER TABLE cbf.escalacao ADD CONSTRAINT pk_escalacao PRIMARY KEY (id_escalacao);
 
ALTER TABLE cbf.jogo ADD CONSTRAINT fk_jogo_campeonato
    FOREIGN KEY (id_campeonato)
    REFERENCES cbf.campeonato (id_campeonato)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.jogo ADD CONSTRAINT fk_jogo_estadio
    FOREIGN KEY (id_estadio)
    REFERENCES cbf.estadio (id_estadio)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.jogo ADD CONSTRAINT fk_jogo_mandante
    FOREIGN KEY (id_clube_mandante)
    REFERENCES cbf.clube (id_clube)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.jogo ADD CONSTRAINT fk_jogo_visitante
    FOREIGN KEY (id_clube_visitante)
    REFERENCES cbf.clube (id_clube);
 
ALTER TABLE cbf.alteracao ADD CONSTRAINT fk_alteracao_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.alteracao ADD CONSTRAINT fk_alteracao_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.evento ADD CONSTRAINT fk_evento_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.evento ADD CONSTRAINT fk_evento_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.documento ADD CONSTRAINT fk_documento_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.equipe_arbitragem ADD CONSTRAINT fk_equipe_arbitragem_arbitro
    FOREIGN KEY (id_arbitro)
    REFERENCES cbf.arbitro (id_arbitro);
 
ALTER TABLE cbf.equipe_arbitragem ADD CONSTRAINT fk_equipe_arbitragem_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo);
 
ALTER TABLE cbf.penalidade ADD CONSTRAINT fk_penalidade_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.penalidade ADD CONSTRAINT fk_penalidade_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.penalidade ADD CONSTRAINT fk_penalidade_atleta
    FOREIGN KEY (id_atleta)
    REFERENCES cbf.atleta (id_atleta)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.estadio ADD CONSTRAINT fk_estadio_cidade
    FOREIGN KEY (id_cidade)
    REFERENCES cbf.cidade (id_cidade)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.escalacao ADD CONSTRAINT fk_escalacao_clube
    FOREIGN KEY (id_clube)
    REFERENCES cbf.clube (id_clube)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.escalacao ADD CONSTRAINT fk_escalacao_atleta
    FOREIGN KEY (id_atleta)
    REFERENCES cbf.atleta (id_atleta)
    ON DELETE CASCADE;
 
ALTER TABLE cbf.escalacao ADD CONSTRAINT fk_escalacao_jogo
    FOREIGN KEY (id_jogo)
    REFERENCES cbf.jogo (id_jogo)
    ON DELETE CASCADE;