-- Estrutura e dados iniciais da rede (serviço Core)

CREATE TABLE linhas (
    id   VARCHAR(10)  PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE paragens (
    id   VARCHAR(10)  PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE linha_paragens (
    linha_id   VARCHAR(10) NOT NULL REFERENCES linhas(id),
    paragem_id VARCHAR(10) NOT NULL REFERENCES paragens(id),
    ordem      INTEGER     NOT NULL,
    PRIMARY KEY (linha_id, ordem)
);

INSERT INTO linhas (id, nome) VALUES
    ('L1', 'Estação Central - Hospital'),
    ('L2', 'Universidade - Praia');

INSERT INTO paragens (id, nome) VALUES
    ('P01', 'Estação Central'),
    ('P02', 'Praça da República'),
    ('P03', 'Hospital'),
    ('P04', 'Universidade'),
    ('P05', 'Praia');

INSERT INTO linha_paragens (linha_id, paragem_id, ordem) VALUES
    ('L1', 'P01', 1), ('L1', 'P02', 2), ('L1', 'P03', 3),
    ('L2', 'P04', 1), ('L2', 'P02', 2), ('L2', 'P05', 3);
