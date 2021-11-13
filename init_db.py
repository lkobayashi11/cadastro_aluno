import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as g:
    connection.executescript(g.read())

cur = connection.cursor()

cur.execute("""INSERT INTO responsavel (nome,rg,cpf,profissao,idempresa) VALUES
            ('Renata Souza', '111111111', '9999999999', 'motorista',1)""")


connection.commit()
connection.close()
