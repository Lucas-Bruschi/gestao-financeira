from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('finance.db')
conn.row_factory = sqlite3.Row

conn.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
);
''')
conn.execute('''
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
);
''')


def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    conn = get_db_connection()
    if request.method == 'POST':
        produto = request.form['produto']
        valor = request.form['valor']
        data = request.form['data']

        conn.execute('INSERT INTO vendas (produto, valor, data) VALUES (?, ?, ?)', (produto, valor, data))
        conn.commit()
        conn.close()


        return redirect(url_for('vendas'))
    
    vendas = conn.execute('SELECT * FROM vendas').fetchall()
    conn.close()
    
    return render_template('vendas.html', vendas=vendas)

@app.route('/despesas', methods=['GET', 'POST'])
def despesas():
    conn = get_db_connection()
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        data = request.form['data']

        conn.execute('INSERT INTO despesas (descricao, valor, data) VALUES (?, ?, ?)', (descricao, valor, data))
        conn.commit()
        conn.close()

        return redirect(url_for('despesas'))
    
    despesas = conn.execute('SELECT * FROM despesas').fetchall()
    conn.close()

    return render_template('despesas.html', despesas=despesas)

if __name__ == '__main__':
    app.run(debug=True)
