from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'biblioteca.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Rotas Livros
@app.route('/livros')
def listar_livros():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()
    return render_template('livro_list.html', livros=livros)

@app.route('/livro/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano = request.form['ano']
        autores = request.form.getlist('autores')
        generos = request.form.getlist('generos')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livros (titulo, ano) VALUES (?, ?)', (titulo, ano))
        livro_id = cursor.lastrowid

        for autor_id in autores:
            cursor.execute('INSERT INTO livros_autores (livro_id, autor_id) VALUES (?, ?)', (livro_id, autor_id))

        for genero_id in generos:
            cursor.execute('INSERT INTO livros_generos (livro_id, genero_id) VALUES (?, ?)', (livro_id, genero_id))

        conn.commit()
        conn.close()
        return redirect(url_for('listar_livros'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM autores')
    autores = cursor.fetchall()
    cursor.execute('SELECT * FROM generos')
    generos = cursor.fetchall()
    conn.close()
    
    return render_template('livro_form.html', autores=autores, generos=generos)

@app.route('/livro/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano = request.form['ano']
        autores = request.form.getlist('autores')
        generos = request.form.getlist('generos')

        cursor.execute('UPDATE livros SET titulo = ?, ano = ? WHERE id = ?', (titulo, ano, id))
        
        cursor.execute('DELETE FROM livros_autores WHERE livro_id = ?', (id,))
        cursor.execute('DELETE FROM livros_generos WHERE livro_id = ?', (id,))
        
        for autor_id in autores:
            cursor.execute('INSERT INTO livros_autores (livro_id, autor_id) VALUES (?, ?)', (id, autor_id))

        for genero_id in generos:
            cursor.execute('INSERT INTO livros_generos (livro_id, genero_id) VALUES (?, ?)', (id, genero_id))

        conn.commit()
        conn.close()
        return redirect(url_for('listar_livros'))

    cursor.execute('SELECT * FROM livros WHERE id = ?', (id,))
    livro = cursor.fetchone()
    cursor.execute('SELECT * FROM autores')
    autores = cursor.fetchall()
    cursor.execute('SELECT * FROM generos')
    generos = cursor.fetchall()
    cursor.execute('SELECT autor_id FROM livros_autores WHERE livro_id = ?', (id,))
    livro_autores = [row['autor_id'] for row in cursor.fetchall()]
    cursor.execute('SELECT genero_id FROM livros_generos WHERE livro_id = ?', (id,))
    livro_generos = [row['genero_id'] for row in cursor.fetchall()]
    conn.close()

    return render_template('livro_form.html', livro=livro, autores=autores, generos=generos, livro_autores=livro_autores, livro_generos=livro_generos)

# Rotas Autores
@app.route('/autores')
def listar_autores():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM autores')
    autores = cursor.fetchall()
    conn.close()
    return render_template('autor_list.html', autores=autores)

@app.route('/autor/adicionar', methods=['GET', 'POST'])
def adicionar_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO autores (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_autores'))
    return render_template('autor_form.html')

@app.route('/autor/editar/<int:id>', methods=['GET', 'POST'])
def editar_autor(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        cursor.execute('UPDATE autores SET nome = ? WHERE id = ?', (nome, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_autores'))
    cursor.execute('SELECT * FROM autores WHERE id = ?', (id,))
    autor = cursor.fetchone()
    conn.close()
    return render_template('autor_form.html', autor=autor)

# Rotas Gêneros
@app.route('/generos')
def listar_generos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generos')
    generos = cursor.fetchall()
    conn.close()
    return render_template('genero_list.html', generos=generos)

@app.route('/genero/adicionar', methods=['GET', 'POST'])
def adicionar_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO generos (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_generos'))
    return render_template('genero_form.html')

@app.route('/genero/editar/<int:id>', methods=['GET', 'POST'])
def editar_genero(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        cursor.execute('UPDATE generos SET nome = ? WHERE id = ?', (nome, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_generos'))
    cursor.execute('SELECT * FROM generos WHERE id = ?', (id,))
    genero = cursor.fetchone()
    conn.close()
    return render_template('genero_form.html', genero=genero)

# Rotas Usuários
@app.route('/usuarios')
def listar_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuario_list.html', usuarios=usuarios)

@app.route('/usuario/adicionar', methods=['GET', 'POST'])
def adicionar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_usuarios'))
    return render_template('usuario_form.html')

@app.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cursor.execute('UPDATE usuarios SET nome = ?, email = ? WHERE id = ?', (nome, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_usuarios'))
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
    usuario = cursor.fetchone()
    conn.close()
    return render_template('usuario_form.html', usuario=usuario)

# Função de Pesquisa
@app.route('/pesquisar', methods=['POST'])
def pesquisa():
    query = request.form['query']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE titulo LIKE ?', ('%' + query + '%',))
    livros = cursor.fetchall()
    conn.close()
    return render_template('resultado_pesquisa.html', livros=livros)

if __name__ == '__main__':
    app.run(debug=True)
