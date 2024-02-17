from flask import Flask, render_template, request, redirect, url_for, Response
from functools import wraps
import sqlite3
from flask import jsonify

app = Flask(__name__)

conn = sqlite3.connect('site.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        gta_name TEXT NOT NULL,
        mta_name TEXT NOT NULL,
        car_id INTEGER NOT NULL,
        image_path TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

conn = sqlite3.connect('site.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weapons (
        gun_id INTEGER NOT NULL,
        gta_name TEXT NOT NULL,
        mta_name TEXT NOT NULL,
        slot_number INTEGER NOT NULL,
        inventory_image TEXT NOT NULL,
        hand_image TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

conn = sqlite3.connect('site.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            object_list TEXT
    )
''')
conn.commit()
conn.close()

conn = sqlite3.connect('site.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS skins (
        skin_id TEXT NOT NULL,
        image TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# Имя пользователя и пароль для базовой аутентификации
ADMIN_USERNAME = 'username'
ADMIN_PASSWORD = 'super-secret-password'

def check_auth(username, password):
    """Проверка имени пользователя и пароля."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def authenticate():
    """Отправка заголовка WWW-Authenticate, чтобы попросить аутентификацию."""
    return Response('Пожалуйста, введите правильное имя пользователя и пароль.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """Декоратор, требующий базовой аутентификации."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/cars')
def cars():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars_data = cursor.fetchall()
    conn.close()
    return render_template('cars.html', cars_data=cars_data)

@app.route('/edit_cars')
@requires_auth
def edit_cars():
    return render_template('edit_cars.html')

@app.route('/add_car', methods=['POST'])
def add_car():
    if request.method == 'POST':
        gta_name = request.form['gta_name']
        mta_name = request.form['mta_name']
        car_id = request.form['car_id']
        image_filename = request.form['image_filename']

        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cars (gta_name, mta_name, car_id, image_path) VALUES (?, ?, ?, ?)', (gta_name, mta_name, car_id, image_filename))
        conn.commit()
        conn.close()

        return redirect(url_for('edit_cars'))
    
@app.route('/weapons')
def weapons():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weapons')
    weapons_data = cursor.fetchall()
    conn.close()

    return render_template('weapons.html', weapons=weapons_data)

@app.route('/edit_weapons')
@requires_auth
def edit_weapons():
    return render_template('edit_weapons.html')

@app.route('/add_weapon', methods=['POST'])
def add_weapon():
    if request.method == 'POST':
        gun_id = request.form['gun_id']
        gta_name = request.form['gta_name']
        mta_name = request.form['mta_name']
        slot_number = request.form['slot_number']
        inventory_image = f"{request.form['inventory_image']}.png"
        hand_image = f"{request.form['hand_image']}.png"
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO weapons (gun_id, gta_name, mta_name, slot_number, inventory_image, hand_image) VALUES (?, ?, ?, ?, ?, ?)',
                       (gun_id, gta_name, mta_name, slot_number, inventory_image, hand_image))
        conn.commit()
        conn.close()

        return redirect(url_for('edit_weapons'))
    
@app.route('/mappings')
def mappings():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects')
    objects_data = cursor.fetchall()
    conn.close()
    return render_template('mappings.html', objects_data=objects_data)

@app.route('/edit_mappings')
def edit_mappings():
    return render_template('edit_mappings.html')

@app.route('/add_mappings', methods=['POST'])
def add_mappings():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        object_list = request.form['object_list']

        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO objects (name, description, object_list) VALUES (?, ?, ?)', (name, description, object_list))
        conn.commit()
        conn.close()

        return redirect(url_for('edit_mappings'))
    
@app.route('/skins')
def skins():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM skins')
    skins = cursor.fetchall()
    conn.close()
    return render_template('skins.html', skins=skins)

@app.route('/edit_skins')
@requires_auth
def edit_skins():
    return render_template('edit_skins.html')

@app.route('/add_skin', methods=['POST'])
def add_skin():
    if request.method == 'POST':
        skin_id = request.form['skin_id']
        image = f"{skin_id}.png"
        category = request.form['category']

        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO skins (skin_id, image, category) VALUES (?, ?, ?)', (skin_id, image, category))
        conn.commit()
        conn.close()

        return redirect(url_for('edit_skins'))

if __name__ == '__main__':
    app.run(debug=True)
