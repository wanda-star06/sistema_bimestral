import sqlite3

def create_db():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # Tabelas principais
    cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ano INTEGER NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS generos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )''')

    # Tabelas de relacionamento muitos-para-muitos
    cursor.execute('''CREATE TABLE IF NOT EXISTS livros_autores (
        livro_id INTEGER,
        autor_id INTEGER,
        FOREIGN KEY (livro_id) REFERENCES livros (id),
        FOREIGN KEY (autor_id) REFERENCES autores (id),
        PRIMARY KEY (livro_id, autor_id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS livros_generos (
        livro_id INTEGER,
        genero_id INTEGER,
        FOREIGN KEY (livro_id) REFERENCES livros (id),
        FOREIGN KEY (genero_id) REFERENCES generos (id),
        PRIMARY KEY (livro_id, genero_id)
    )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
