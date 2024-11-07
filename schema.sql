CREATE TABLE IF NOT EXISTS usuario (id INTEGER PRIMARY KEY AUTOINCREMENT,nome_usuario TEXT NOT NULL UNIQUE, chave TEXT NOT NULL, chave_controle BOOLEAN);

CREATE TABLE IF NOT EXISTS senhas (
    senha TEXT NOT NULL,
    nome_senha TEXT NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    PRIMARY KEY (nome_senha, id_usuario));