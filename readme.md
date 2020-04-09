$ pipenv shell
$ python app.py runserver


- - - crear ruta para MOSTRAR TODA LA LISTA ("/all)

1) importar la clase Queue para agregarle todas las funciones q son creadas en myqueue.py

2) agregar contactos en self._queue con nombre y telefono en myqueue

3) agregar account id y el token que esta en la pagina de twilio 

4) en myqueue configurar la fx get_queue haciendo un return para q me de la lista q esta dentro del array

5) users = _queue.get_queue
para q me de la lista q esta en la clase queue y q me lo retorne como un jsonify para q lo lea en formato JSON los usuarios

6) en html si ponfo /all en el url, me muestra toda la lista



- - - crear ruta para  "/new"
1) capturar los datos q quiero mandar, validanolos como si fuera un formulario

    if not request.is_json:
        return jsonify({"msg": "Missing JSON request"}), 400

si no esta mandando la info en formato JSON, manda un mensaje de error


2) validar si vienen los datos 

    name = request.json.get('name', None)
    phone = request.json.get('phone', None)


3) validar q la info no sea None ni vacio

    if not name or name == '':
        return jsonify({"msg": "Missing Field Name in request"}), 400
    if not phone or phone == '':
        return jsonify({"msg": "Missing Field Phone in request"}), 400


4) abrir insmonia

    4.1) creo una carpeta API REST SMS

    4.2) creo nuevo request GET Queue q va a ser la ruta "/all"
        con json como body me muestra toda la lista

    4.3) creo un metodo POST con body JSON con ruta "/new"

    4.4) para q se vea el contenido, el body se debe agregar {} y me va a dar el mensaje "name request"

    4.5) si se pone
    { 
        "name": "",                     me da msg de name vacio
        "phone: ""
    }

    4.6) si se agrega name
    { 
        "name": "Juan",                  me da mensaje de phone
        "phone: ""
    }


5) fx enqueue agrega una persona a la lista 
creo un elemento para retornar el resultao de agregar una persona a la lista + un mensaje con el resultado de la persona y telefono q se quiere agregar

    item = {
        "name": name,
        "phone": phone
    }

    result = objQueue.enqueue(item)
    return jsonify({"msg": "User added to the list", "result": result}), 200


6) agregar elementos a la lista o array
    usando la fx append a traves del self para acceder al elemento queue y agregarlo

    self._queue.append(item)


7) en insmonmia
    a) en el POST agregar una nueva persona
    b) en el GET se muestra toda la lista con la persona agregada 



- - - ELIMINAR UNA PERSONA DE LA LISTA crear ruta "/next" recibe el metodo GET usando la fx dequeue
  
1) para retornar el elemento q fue procesado llamando a la fx dequeue 
    result = objQueue.dequeue()
    return jsonify({"msg": "User deleted from the list", "result": result}), 200


2) se debe cambiar la fx dequeue para eliminar una persona de la lista segun el mode FIFO o LIFO
    
        if self._mode == 'FIFO':
            item = self._queue.pop(0) => para eliminar el primer elemento de la lista FIFO
        else:
            item = self._queue.pop() => para eliminar el ultimo elemento de la lista LIFO


3) INSOMNIA
    3.1) crear DELETE

    3.2) copiar la ruta con "/next"

    3.3) si pongo send en cada contacto q me muestra, lo estoy eliminando

    3.4) cuando se eliminan todos, da error porq la lista esta vacia. Se tiene q validar el mommeto de hacer delete nuevamente si la lista esta vacia o no


4) para validar el mommeto de hacer delete al ultimo debe mandar un msg si la lista esta vacia o no con la fx size > 0

        if self.size() > 0:
            if self._mode == 'FIFO':
                item = self._queue.pop(0)# para obtener el primer elemento de la lista
            else:
                item = self._queue.pop()# si no le paso parametro, elimina el ultimo o sea para usar LIFO
            return item
        else: 
            return "La lista esta vacia"


5) IMSOMNIA
    si elimino todo lo de POST, al final me da un mensaje q la lista esta vacia


6) para usar LIFO, se debe cambiar el _node a LIFO y probar en insmnia. se eliminaria desde atras a adelante


- - MANDAR SMS cuando se registra el usuario y cuando es prosesado de la fila

1) se manda despues de hacer la validación de si es FIFO o LIFO y antes del return en la fx dequeue
            # Envio del SMS
            message = self.client.messages.create(
                body = "Gracias " + item["name"] + ", por venir lo esperamos pronto",
                to = item["phone"],
                from_ = "+xxxxxxxxxxxxxxxxxxxx" 
            )

            result = {
                "item": item,
                "message": {
                    "sid": message.sid,
                    "status": message.status
                }
            }


2) el mensaje debe tener un body, un to para saber a quien y from es de q numero manda el mensaje

        msg = ""
        if self.size() > 0:
            msg = "Usted tiene " + str(self.size()) + " personas por delante"
        else:
            msg = "Usted es el proximo a ser atendido"

        message = self.client.messages.create(
            body = "Bievenido " + item["name"] + ", " + msg,
            to = item["phone"],#el telefono de cada persona
            from_ = "+xxxxxxxxxxxxxxxxxxxxxx"#telefono de twilio
        )

3) se debe mandar mensaje a la persona cuando se va de la lista en el dequeue

            message = self.client.messages.create(
                body = "Gracias " + item["name"] + ", por venir lo esperamos pronto",
                to = item["phone"],
                from_ = "+xxxxxxxxxxxxxxxxxxxxxxxx" 
            )

4) para saber el resultado del mensaje 

        result = {
            "item": item,
            "message": {
                "sid": message.sid,
                "status": message.status
            }
        }

