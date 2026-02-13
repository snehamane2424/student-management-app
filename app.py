from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Database Configuration (Use RDS endpoint later)
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
        conn.commit()
        conn.close()

        return redirect('/view')
    return render_template('add_student.html')

@app.route('/view')
def view_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
