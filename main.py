import json
from flask import Flask, request, redirect, url_for, render_template
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conectar a MongoDB
url = "https://us-east-2.aws.data.mongodb-api.com/app/data-zonztjc/endpoint/data/v1/action/insertOne"
find_url = "https://us-east-2.aws.data.mongodb-api.com/app/data-zonztjc/endpoint/data/v1/action/find"
update_url = "https://us-east-2.aws.data.mongodb-api.com/app/data-zonztjc/endpoint/data/v1/action/updateOne"
delete_url = "https://us-east-2.aws.data.mongodb-api.com/app/data-zonztjc/endpoint/data/v1/action/deleteOne"

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'apiKey': 'ayhZJpqfAO5luBODict0E2jXNalV55ANTKF9tcqTq4ycHyOQ8NoCxy0PcyQ5xlE0'
}

# Índice principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellidos = request.form['apellidos'].strip()
        edad = request.form['edad'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        hashed_password = generate_password_hash(password)

        payload = {
            "dataSource": "Equipo",
            "database": "Prueba_datos",
            "collection": "Datos",
            "document": {
                "nombre": nombre,
                "apellidos": apellidos,
                "edad": edad,
                "fecha_nacimiento": fecha_nacimiento,
                "email": email,
                "password": hashed_password
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            return render_template('index')
    return render_template('registro.html')


# Ruta de inicio de sesión
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    query_payload = {
        "dataSource": "Equipo",
        "database": "Prueba_datos",
        "collection": "Datos",
        "filter": {
            "email": email
        }
    }

    response = requests.post(find_url, headers=headers, data=json.dumps(query_payload))

    if response.status_code == 200:
        user_data = response.json()
        documents = user_data.get('documents', [])

        if len(documents) > 0:
            user = documents[0]
            if check_password_hash(user['password'], password):
                return redirect(url_for('inicio'))
            else:
                return "Contraseña incorrecta"
        else:
            return "Usuario no encontrado"
    else:
        return f"Error al buscar usuario: {response.text}"

# Ruta de configuración de dispositivos
@app.route('/inicio')
def inicio():
    query_payload = {
        "dataSource": "Equipo",
        "database": "Prueba_datos",
        "collection": "ips",
        "filter": {}
    }

    response = requests.post(find_url, headers=headers, data=json.dumps(query_payload))

    if response.status_code == 200:
        datos = response.json().get('documents', [])
        return render_template('inicio.html', datos=datos)
    else:
        return f"Error al obtener datos: {response.text}"

# Ruta para guardar datos
@app.route('/guarda_datos', methods=['POST'])
def guarda_datos():
    ip = request.form['ip']
    nom_dis = request.form['nom_dis']
    nom_soft = request.form['nom_soft']
    version = request.form['version']
    fecha_inst = request.form['fecha_inst']
    fecha_actua = request.form['fecha_actua']
    nom_prove = request.form['nom_prove']
    estado = request.form['estado']

    payload = {
        "dataSource": "Equipo",
        "database": "Prueba_datos",
        "collection": "ips",
        "document": {
            "IP": ip,
            "Nombre_Dispositivo": nom_dis,
            "Nombre_Software": nom_soft,
            "Version": version,
            "Fecha_Instalacion": fecha_inst,
            "Fecha_Actualizacion": fecha_actua,
            "Proveedor": nom_prove,
            "Estado": estado
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return redirect(url_for('inicio'))


# Ruta para modificar los datos
@app.route('/modificar_dato/<string:document_id>', methods=['POST'])
def modificar_dato(document_id):
    ip = request.form['ip']
    nom_dis = request.form['nom_dis']
    nom_soft = request.form['nom_soft']
    version = request.form['version']
    fecha_inst = request.form['fecha_inst']
    fecha_actua = request.form['fecha_actua']
    nom_prove = request.form['nom_prove']
    estado = request.form['estado']

    payload = {
        "dataSource": "Equipo",
        "database": "Prueba_datos",
        "collection": "ips",
        "filter": { "_id": { "$oid": document_id } },
        "update": {
            "$set": {
                "IP": ip,
                "Nombre_Dispositivo": nom_dis,
                "Nombre_Software": nom_soft,
                "Version": version,
                "Fecha_Instalacion": fecha_inst,
                "Fecha_Actualizacion": fecha_actua,
                "Proveedor": nom_prove,
                "Estado": estado
            }
        }
    }

    response = requests.post(update_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return redirect(url_for('inicio'))
    else:
        return f"Error al modificar datos: {response.text}"

# Ruta para eliminar los datos
@app.route('/eliminar_dato/<string:dato_id>', methods=['POST'])
def eliminar_dato(dato_id):
    payload = {
        "dataSource": "Equipo",
        "database": "Prueba_datos",
        "collection": "ips",
        "filter": { "_id": { "$oid": dato_id } }
    }

    response = requests.post(delete_url, headers=headers, data=json.dumps(payload))

    # Verificar si la eliminación fue exitosa
    if response.status_code == 200:
        return redirect(url_for('inicio'))
    elif response.status_code == 204:
        return redirect(url_for('inicio'))
    else:
        return f"Error al eliminar datos: {response.text}"

if __name__ == '__main__':
    app.run(debug=True, port=1200)
