import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



def get_post(post_id):
    conn = get_db_connection()
    responsavel = conn.execute('SELECT r.idresponsavel, r.created, r.nome, r.rg, r.cpf, r.profissao, e.nome as empresa '
                               ' FROM responsavel r JOIN empresa e ON r.idempresa = e.idempresa '
                               ' and idresponsavel = ?',
                               (post_id,)).fetchone()
    conn.close()
    if responsavel is None:
        abort(404)
    return responsavel

def get_post_aluno(post_aluno_id):
    conn = get_db_connection()

    aluno = conn.execute('SELECT a.idaluno, a.created, a.nome, a.rg, a.certidao_nasc, a.dt_nasc, a.naturalidade,'
                         ' a.uf,  a.endereco, a.genero , a.qtdirmao, a.qtdirma, a.grau_escolaridade, a.horario,'
                         ' a.carterinha_vacina, a.informacao, a.telefone, r.nome as responsavel , e.nome as escola1,'
                         ' ifnull(i.remedio,"Nada Consta") as remedio '
                         ' FROM aluno a '
                         ' INNER JOIN responsavel r ON a.idresponsavel = r.idresponsavel '
                         ' INNER JOIN escola e ON a.idescola = e.idescola '
                         ' INNER JOIN informacoes i ON a.idinformacao = i.idinformacao '
                         ' and idaluno = ?',
                         (post_aluno_id,)).fetchone()

    conn.close()
    if aluno is None:
        abort(404)
    return aluno


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefg123456'


#----------------------------------Responsável -------------------------------------------------------------------

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
    empresaList = conn.execute('SELECT * FROM empresa order by nome').fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        rg = request.form['rg']
        profissao = request.form['profissao']
        empresa = request.form['empresa']

        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO responsavel (nome, cpf, rg, profissao, idempresa) VALUES (?, ?, ?, ?, ?)',
                         (nome, cpf, rg, profissao, empresa))
            conn.commit()
            conn.close()
            return redirect(url_for('view_responsavel'))


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
        empresa= request.form['empresa']

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


#---------------------------------------Aluno -------------------------------------------------------------------

@app.route('/')
def index():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM aluno').fetchall()
    conn.close()
    return render_template('index.html', alunos=alunos)


@app.route('/aluno/<int:post_alunoid>')
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
   # escola = ''
    grau = ''
    horario = ''
    vacina = ''
    informacao = ''
    telefone = ''
    responsavel = ''
    escola1 = ''
    remedio = ''

    conn = get_db_connection()
    responsavelList = conn.execute('SELECT * FROM responsavel order by nome').fetchall()

    conn = get_db_connection()
    escolaList = conn.execute('SELECT * FROM escola order by nome').fetchall()

    conn = get_db_connection()
    remedioList = conn.execute('SELECT * FROM informacoes order by remedio').fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        rg = request.form['rg']
        certidao = request.form['certidao']
        dtnasc = request.form['dtnasc']
        naturalidade = request.form['naturalidade']
        uf = request.form['uf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        genero = request.form['genero']
        qtdirmao = request.form['qtdirmao']
        qtdirma = request.form['qtdirma']
        #escola = request.form['escola']
        grau = request.form['grau']
        horario = request.form['horario']
        vacina = request.form['vacina']
        informacao = request.form['informacao']
        responsavel = request.form['responsavel']
        escola1 = request.form['escola1']
        remedio = request.form['remedio']

        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO aluno (nome, rg, certidao_nasc, dt_nasc,naturalidade,UF,'
                         'endereco,genero,qtdirmao,qtdirma, grau_escolaridade,horario,carterinha_vacina,'
                         'informacao,telefone, idresponsavel, idescola, idinformacao) '
                         'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (nome, rg, certidao, dtnasc, naturalidade, uf, endereco, genero, qtdirmao, qtdirma,
                          grau, horario, vacina, informacao, telefone, responsavel, escola1, remedio))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('createaluno.html', nome=nome, rg=rg, certidao=certidao, dtnasc=dtnasc,
                           naturalidade=naturalidade, uf=uf, endereco=endereco, genero=genero,
                           qtdirmao=qtdirmao, qtdirma=qtdirma,
                           grau=grau, horario=horario, vacina=vacina, informacao=informacao, telefone=telefone,
                           responsavel=responsavel, responsavelList=responsavelList, escola1=escola1, escolaList=escolaList,
                           remedio=remedio, remedioList=remedioList)


@app.route('/aluno/<int:id>/edit', methods=('GET', 'POST'))
def edit_aluno(id):
    aluno = get_post_aluno(id)

    conn = get_db_connection()
    responsavelList = conn.execute('SELECT * FROM responsavel order by nome').fetchall()

    conn = get_db_connection()
    escolaList = conn.execute('SELECT * FROM escola order by nome').fetchall()

    conn = get_db_connection()
    remedioList = conn.execute('SELECT * FROM informacoes order by remedio').fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        rg = request.form['rg']
        certidao = request.form['certidao']
        dtnasc = request.form['dtnasc']
        naturalidade = request.form['naturalidade']
        uf = request.form['uf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        genero = request.form['genero']
        qtdirmao = request.form['qtdirmao']
        qtdirma = request.form['qtdirma']
        escola = request.form['escola']
        grau = request.form['grau']
        horario = request.form['horario']
        vacina = request.form['vacina']
        informacao = request.form['informacao']
        responsavel = request.form['responsavel']
        remedio = request.form['remedio']

        if not nome:
            flash('Digite o nome!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE aluno SET nome = ?, rg = ? , certidao_nasc =? , dt_nasc =? , naturalidade = ? ,'
                         ' UF = ?, endereco = ? ,genero = ?,qtdirmao =? ,qtdirma = ?, escola = ? ,'
                         ' grau_escolaridade = ? ,horario =? ,carterinha_vacina =? ,informacao =?, telefone = ?'
                         ' WHERE idaluno = ?',
                         (nome, rg, certidao, dtnasc,naturalidade,uf,endereco,genero,qtdirmao,qtdirma,escola,grau ,
                          horario ,vacina ,informacao, telefone, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('editaluno.html', post=aluno, responsavelList=responsavelList, escolaList=escolaList,
                          remedioList=remedioList)

@app.route('/aluno/<int:id>/delete', methods=('POST',))
def delete_aluno(id):
    post = get_post_aluno(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM aluno WHERE idaluno = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluído com sucesso!'.format(post['nome']))
    return redirect(url_for('index'))


# ----------------------------------------------Informaçoes médicas -----------------------------------------

def get_post_informacao(post_informacaoid):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM informacoes WHERE idinformacao = ?',
                        (post_informacaoid,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/informacao/<int:post_informacaoid>')
def post_informacao(post_informacaoid):
    informacao = get_post_informacao(post_informacaoid)
    return render_template('postinformacao.html', post=informacao)


@app.route('/informacao')
def view_informacao():
    conn = get_db_connection()
    informacoes = conn.execute('SELECT * FROM informacoes').fetchall()
    conn.close()
    return render_template('informacao.html', posts=informacoes)


@app.route('/informacao/create', methods=('GET', 'POST'))
def create_informacao():
    remedio = ''
    informacao = ''

    if request.method == 'POST':
        remedio = request.form['remedio']
        informacao = request.form['informacao']

        if not remedio:
            flash('Digite o remedio!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO informacoes (informacao, remedio) VALUES (?, ?)',
                         (informacao, remedio))
            conn.commit()
            conn.close()
            return redirect(url_for('view_informacao'))

    return render_template('createinformacao.html', remedio=remedio , informacao=informacao)

@app.route('/informacao/<int:id>/edit', methods=('GET', 'POST'))
def edit_informacao(id):
    informacao = get_post_informacao(id)

    if request.method == 'POST':
        remedio = request.form['remedio']
        informacao = request.form['informacao']

        if not remedio:
            flash('Digite o remédio!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE informacoes SET informacao = ?, remedio = ? '
                         ' WHERE idinformacao = ?',
                         (informacao, remedio, id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_informacao'))

    return render_template('editinformacao.html', post=informacao)



# ----------------------------------------------Empresa -----------------------------------------

def get_post_empresa(post_empresaid):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM empresa WHERE idempresa = ?',
                        (post_empresaid,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/empresa/<int:post_empresaid>')
def post_empresa(post_empresaid):
    empresa = get_post_empresa(post_empresaid)
    return render_template('postempresa.html', empresa=empresa)


@app.route('/empresa')
def view_empresa():
    conn = get_db_connection()
    empresas = conn.execute('SELECT * FROM empresa').fetchall()
    conn.close()
    return render_template('empresa.html', posts=empresas)

@app.route('/empresa/create', methods=('GET', 'POST'))
def create_empresa():
    nome = ''

    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Digite a empresa!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO empresa (nome) VALUES (?)',
                         (nome,))
            conn.commit()
            conn.close()
            return redirect(url_for('view_empresa'))

    return render_template('createempresa.html', nome=nome)


@app.route('/empresa/<int:id>/edit', methods=('GET', 'POST'))
def edit_empresa(id):
    empresa = get_post_empresa(id)

    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Digite a empresa!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE empresa SET nome = ? '
                         ' WHERE idempresa = ?',
                         (nome, id))
            conn.commit()
            conn.close()
            return redirect(url_for('empresa'))

    return render_template('editempresa.html', post=empresa)


# ----------------------------------------------Escola -----------------------------------------

def get_post_escola(post_escolaid):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM escola WHERE idescola = ?',
                        (post_escolaid,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/escola/<int:post_escolaid>')
def post_escola(post_escolaid):
    escola = get_post_escola(post_escolaid)
    return render_template('postescola.html', escola=escola)


@app.route('/escola')
def view_escola():
    conn = get_db_connection()
    escolas = conn.execute('SELECT * FROM escola').fetchall()
    conn.close()
    return render_template('escola.html', posts=escolas)

@app.route('/escola/create', methods=('GET', 'POST'))
def create_escola():
    nome = ''

    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Digite a escola!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO escola (nome) VALUES (?)',
                         (nome,))
            conn.commit()
            conn.close()
            return redirect(url_for('view_escola'))

    return render_template('createescola.html', nome=nome)

@app.route('/escola/<int:id>/edit', methods=('GET', 'POST'))
def edit_escola(id):
    escola = get_post_escola(id)

    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Digite a escola!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE escola SET nome = ? '
                         ' WHERE idescola = ?',
                         (nome, id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_escola'))

    return render_template('editescola.html', post=escola)


