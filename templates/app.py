from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)
app.config['DATABASE'] = 'attendance.db'

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        date = request.form['date']
        student_ids = request.form.getlist('student_ids')
        mark_attendance_in_database(date, student_ids)
        return redirect(url_for('home'))
    else:
        return render_template('mark_attendance.html')

@app.route('/view_attendance', methods=['GET', 'POST'])
def view_attendance():
    if request.method == 'POST':
        date = request.form['date']
        attendance = get_attendance_from_database(date)
        return render_template('view_attendance.html', date=date, attendance=attendance)
    else:
        return render_template('view_attendance_form.html')



def mark_attendance_in_database(date, student_ids):
    conn = get_db_connection()
    for student_id in student_ids:
        conn.execute('INSERT INTO attendance (date, student_id) VALUES (?, ?)', (date, student_id))
    conn.commit()
    conn.close()

def get_attendance_from_database(date):
    conn = get_db_connection()
    cursor = conn.execute('SELECT student_id FROM attendance WHERE date = ?', (date,))
    attendance = [row['student_id'] for row in cursor.fetchall()]
    conn.close()
    return attendance

if __name__ == '__main__':
    init_db()
    app.run(debug=True)