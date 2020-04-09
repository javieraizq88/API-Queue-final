from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db
from myqueue import Queue


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

objQueue = Queue()# trae las funciones de la clase queue de myqueue.py

@app.route('/')
def main():
    return render_template('index.html')

# if method == GET va a usar self._queue y manda mensaje
# if method == GET (all) mostrat arreglo self.queue
# if method == POST

@app.route('/new', methods=['POST'])# recibe a 1 y llama a next
def new_element():
    if not request.is_json:# si no viene en formato json, devuelve un sjonify
        return jsonify({"msg": "Missing JSON request"}), 400
    
    name = request.json.get('name', None)# elegir q persona agregar a la lista
    phone = request.json.get('phone', None)# elegir q persona agregar a la lista

    if not name or name == '':
        return jsonify({"msg": "Missing Field Name in request"}), 400
    if not phone or phone == '':
        return jsonify({"msg": "Missing Field Phone in request"}), 400

    item = {
        "name": name,
        "phone": phone
    }

    result = objQueue.enqueue(item)

    return jsonify({"msg": "User added to the list", "result": result}), 200


@app.route('/next')# la persona avanza y le llega un mensaje
def next_element():
    result = objQueue.dequeue()
    return jsonify({"msg": "User deleted from the list", "result": result}), 200

@app.route('/all')# me da la lista completa
def all_element():
    users = objQueue.get_queue()
    return jsonify(users), 200
# entrega la lista de las personas q estan en la clase Queue


if __name__ == '__main__':
    manager.run()