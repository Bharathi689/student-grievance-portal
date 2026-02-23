
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('grievances.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT,
            name TEXT,
            department TEXT,
            year TEXT,
            category TEXT,
            subject TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        data = (
            request.form['ticket'],
            request.form['name'],
            request.form['department'],
            request.form['year'],
            request.form['category'],
            request.form['subject'],
            request.form['description']
        )
        conn = sqlite3.connect('grievances.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO grievances(ticket, name, department, year, category, subject, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/manage')
    return render_template('submit_grievance.html')

@app.route('/manage')
def manage():
    conn = sqlite3.connect('grievances.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grievances")
    rows = cursor.fetchall()
    conn.close()
    return render_template('manage_grievances.html', grievances=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
