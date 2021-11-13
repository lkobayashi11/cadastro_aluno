import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    responsavel = conn.execute('SELECT * FROM responsavel WHERE idresponsavel = ?',
                               (post_id,)).fetchone()
    conn.close()
    if responsavel is None:
        abort(404)
    return responsavel

def get_post_aluno(post_aluno_id):
    conn = get_db_connection()
    aluno = conn.execute('SELECT * FROM aluno WHERE idaluno = ?',
                         (post_aluno_id,)).fetchone()
    conn.close()
    if aluno is None:
        abort(404)
    return aluno


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefg123456'


@app.route('/')
def index():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM aluno').fetchall()
    conn.close()
    return render_template('index.html', alunos=alunos)


@app.route('/responsavel')
def view_responsavel():
    conn = get_db_connection()
    responsaveis = conn.execute('SELECT * FROM responsavel').fetchall()
    conn.close()
    return render_template('responsavel.html', posts=responsaveis)


@app.route('/responsavel/<int:post_id>')
def post(post_id):
    responsavel = get_post(post_id)
    return render_template('post.html', post=responsavel)


@app.route('/responsavel/create', methods=('GET', 'POST'))
def create():
    nome = ''
    cpf = ''
    rg = ''
    profissao = ''
    idempresa = 0
    empresa = ''

    conn = get_db_connection()
    empresaList = conn.execute('SELECT * FROM empresa').fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        rg = request.form['rg']
        profissao = request.form['profissao']
        empresa = request.form['empresa']

       # conn = get_db_connection()
       # idempresa = conn.execute('SELECT idempresa FROM empresa WHERE nome = (?);', (empresa,))


        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO responsavel (nome, cpf, rg, profissao, idempresa) VALUES (?, ?, ?, ?, ?)',
                         (nome, cpf, rg, profissao, idempresa))
            conn.commit()
            conn.close()
            return redirect(url_for('view_responsavel'))

    # conn = get_db_connection()
    # empresaList=conn.execute('SELECT * FROM empresa').fetchall()

    return render_template('create.html', nome=nome, cpf=cpf, rg=rg, profissao=profissao,
                           empresa=empresa, empresaList=empresaList)


@app.route('/responsavel/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    responsavel = get_post(id)

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        rg = request.form['rg']
        profissao = request.form['profissao']

        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE responsavel SET nome = ?, cpf = ?, rg = ? , profissao = ?'
                         ' WHERE idresponsavel = ?',
                         (nome, cpf, rg, profissao, id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_responsavel'))

    return render_template('edit.html', post=responsavel)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM responsavel WHERE idresponsavel = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluído com sucesso!'.format(post['nome']))
    return redirect(url_for('view_responsavel'))

#---------------------Aluno -------------------------------------------------------------------

@app.route('/<int:post_alunoid>')
def post_aluno(post_alunoid):
    aluno = get_post_aluno(post_alunoid)
    return render_template('postaluno.html', aluno=aluno)

@app.route('/aluno/create', methods=('GET', 'POST'))
def create_aluno():
    nome = ''
    rg = ''
    certidao = ''
    dtnasc = ''
    naturalidade = ''
    uf = ''
    endereco = ''
    genero = ''
    qtdirmao = ''
    qtdirma = ''
    escola = ''
    grau = ''
    horario = ''
    vacina = ''
    informacao = ''


    if request.method == 'POST':
        nome = request.form['nome']
        rg = request.form['rg']
        certidao = request.form['certidao']
        dtnasc = request.form['dtnasc']
        naturalidade = request.form['naturalidade']
        uf = request.form['uf']
        endereco = request.form['endereco']
        genero = request.form['genero']
        qtdirmao = request.form['qtdirmao']
        qtdirma = request.form['qtdirma']
        escola = request.form['escola']
        grau = request.form['grau']
        horario = request.form['horario']
        vacina = request.form['vacina']
        informacao = request.form['informacao']

        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO aluno (nome, rg, certidao_nasc, dt_nasc,naturalidade,UF,'
                         'endereco,genero,qtdirmao,qtdirma,escola,grau_escolaridade,horario,carterinha_vacina,informacao) '
                         'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (nome, rg, certidao, dtnasc,naturalidade,uf,endereco,genero,qtdirmao,qtdirma,escola,grau,horario,vacina,informacao))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('createaluno.html', nome=nome, rg=rg, certidao=certidao, dtnasc=dtnasc,naturalidade=naturalidade,
                           uf=uf ,endereco=endereco,genero=genero,qtdirmao=qtdirmao,qtdirma=qtdirma,escola=escola,
                           grau=grau,horario=horario,vacina=vacina,informacao=informacao)


@app.route('/aluno/<int:id>/edit', methods=('GET', 'POST'))
def edit_aluno(id):
    aluno = get_post_aluno(id)

    if request.method == 'POST':
        nome = request.form['nome']
        rg = request.form['rg']
        certidao = request.form['certidao']
        dtnasc = request.form['dtnasc']
        naturalidade = request.form['naturalidade']
        uf = request.form['uf']
        endereco = request.form['endereco']
        genero = request.form['genero']
        qtdirmao = request.form['qtdirmao']
        qtdirma = request.form['qtdirma']
        escola = request.form['escola']
        grau = request.form['grau']
        horario = request.form['horario']
        vacina = request.form['vacina']
        informacao = request.form['informacao']

        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE aluno SET nome = ?, rg = ? , certidao_nasc =? , dt_nasc =? ,'
                         'naturalidade = ? ,UF = ?, endereco = ? ,genero = ?,qtdirmao =? ,qtdirma = ?,'
                         'escola = ? , grau_escolaridade = ? ,horario =? ,carterinha_vacina =? ,informacao =? '
                         ' WHERE idaluno = ?',
                         (nome, rg, certidao, dtnasc,naturalidade,uf,endereco,genero,qtdirmao,qtdirma,escola,grau ,horario ,vacina ,informacao, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('editaluno.html', post=aluno)

@app.route('/aluno/<int:id>/delete', methods=('POST',))
def delete_aluno(id):
    post = get_post_aluno(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM aluno WHERE idaluno = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluído com sucesso!'.format(post['nome']))
    return redirect(url_for('index'))