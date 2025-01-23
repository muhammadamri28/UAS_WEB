from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'a8y6c.h.filess.io'
app.config['MYSQL_USER'] = 'taskmanager_anyonecamp'
app.config['MYSQL_PASSWORD'] = 'ea41c11088690f0866fdd8321c82d8fe68aa7436'
app.config['MYSQL_DB'] = 'taskmanager_anyonecamp'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user['id'], user['username'])
    return None

def add_default_admin():
    """Menambahkan admin default jika belum ada dalam database."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = 'vito'")
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (username, password) VALUES ('vito', 'vito123')")
        mysql.connection.commit()
        print("Admin default berhasil ditambahkan: username='vito', password='vito123'")
    else:
        print("Admin default sudah ada dalam database.")

@app.before_request
def test_db_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")  
        print("Database connected successfully!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Routes utama
@app.route('/')
@login_required
def index():
    """Halaman utama menampilkan daftar tugas."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login untuk pengguna."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash('Login gagal. Periksa username dan password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout pengguna."""
    logout_user()
    return redirect(url_for('login'))

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage_tasks():
    """Halaman untuk menambahkan dan melihat tugas."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute('INSERT INTO tasks (title, description) VALUES (%s, %s)', (title, description))
        mysql.connection.commit()
        flash('Tugas berhasil ditambahkan.')

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    return render_template('manage_tasks.html', tasks=tasks)

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    """Menghapus tugas berdasarkan ID."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM tasks WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Tugas berhasil dihapus.')
    return redirect(url_for('manage_tasks'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """Mengedit tugas berdasarkan ID."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute('UPDATE tasks SET title = %s, description = %s WHERE id = %s', (title, description, id))
        mysql.connection.commit()
        flash('Tugas berhasil diperbarui.')
        return redirect(url_for('manage_tasks'))

    cursor.execute('SELECT * FROM tasks WHERE id = %s', (id,))
    task = cursor.fetchone()

    if task is None:
        flash('Tugas tidak ditemukan.')
        return redirect(url_for('manage_tasks'))

    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        add_default_admin()
    app.run(debug=True)
