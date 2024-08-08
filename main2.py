from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Conectar a MongoDB
client = MongoClient("mongodb+srv://ll5415299:iPPfS3Z6lBcyaRxG@equipo.xdg2u.mongodb.net/")
db = client.Prueba_datos
collection = db.Datos
#Index principal
@app.route('/')
def index():
    return render_template('index.html')

#ruta de form action
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellidos = request.form['apellidos'].strip()
        edad = request.form['edad'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Verificar si el email ya existe
        if collection.find_one({"email": email}):
            return "El email ya está registrado"

        # Hashear la contraseña
        password_hashed = generate_password_hash(password)

        # Insertar el nuevo usuario en la base de datos
        collection.insert_one({
            "nombre": nombre,
            "apellidos": apellidos,
            "edad": edad,
            "fecha_nacimiento": fecha_nacimiento,
            "email": email,
            "password": password_hashed
        })

        return redirect(url_for('index'))
    return render_template('registro.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    try:
        # Buscar el usuario por email
        user = collection.find_one({"email": email})

        if user:
            # Obtener el valor del campo 'password'
            password_stored = user.get('password')
            if password_stored:
                # Verificar el hash de la contraseña almacenada
                if check_password_hash(password_stored, password):
                    return redirect(url_for('inicio'))
                else:
                    return "Contraseña incorrecta"
            else:
                return "Campo de contraseña no encontrado en el documento"
        else:
            return "Usuario no encontrado"
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

if __name__ == '__main__':
    app.run(debug=True, port=1200)
