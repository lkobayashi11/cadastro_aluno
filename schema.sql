DROP TABLE IF EXISTS responsavel;

CREATE TABLE responsavel (
   idresponsavel INTEGER PRIMARY KEY AUTOINCREMENT,
   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   nome varchar(80) NOT NULL,
   rg varchar(15),
   cpf varchar(15),
   profissao varchar (20),
   idempresa integer,
   FOREIGN KEY (idempresa)
       REFERENCES empresa(idempresa)
 );