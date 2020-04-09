# FIFO = # First In - First Out (Primer en Entrar - Primero en Salir)
# Debo eliminar siempre el primero de la lista

# LIFO = # Last In - First Out (Ultimo en Entrar - Primero en Salir)
# Debo eliminar siempre el ultimo de la lista
from twilio.rest import Client

class Queue:

    def __init__(self):# el init es el constructor de JS
        self.account_sid = 'xxxxxxxxxxxxxxxxx'# lo saque de la pag de twilio
        self.auth_token = 'xxxxxxxxxxxxxxxxxxxxx'# lo saque de la pag de twilio
        self.client = Client(self.account_sid, self.auth_token)# son los elementos q pide twilio
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item): 
      
        # Envio del SMS
        msg = ""
        if self.size() > 0:
            msg = "Usted tiene " + str(self.size()) + " personas por delante"
        else:
            msg = "Usted es el proximo a ser atendido"

        message = self.client.messages.create(
            body = "Bievenido " + item["name"] + ", " + msg,
            to = item["phone"],#el telefono de cada persona
            from_ = "+xxxxxxxxxxxxxxx"#telefono de twilio
        )

        self._queue.append(item)# agrega persona a la lista

        result = {
            "item": item,
            "message": {
                "sid": message.sid,
                "status": message.status
            }
        }
        return result
        
        
    def dequeue(self):# saca a la persona de la lista y depende si es FIFO o LIFO

        if self.size() > 0:
            if self._mode == 'FIFO':
                item = self._queue.pop(0)# para obtener el primer elemento de la lista
            else:
                item = self._queue.pop()# si no le paso parametro, elimina el ultimo o sea para usar LIFO

            # Envio del SMS
            message = self.client.messages.create(
                body = "Gracias " + item["name"] + ", por venir lo esperamos pronto",
                to = item["phone"],
                from_ = "+xxxxxxxxxxxx" 
            )

            result = {
                "item": item,
                "message": {
                    "sid": message.sid,
                    "status": message.status
                }
            }
            
            return result
        else:
            return "Lista vacia"
        

    def get_queue(self):# me da los elementos dentro del array
        return self._queue

    def size(self):# me da el tamañano de la fila
        return len(self._queue)


'''
message = self.client.messages.create(
         body="Join Earth's mightiest heroes. Like Kevin Bacon.",
         to='+15558675310',
         from_="+19254013172"
     )

print(message)


{
  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "api_version": "2010-04-01",
  "body": "Join Earth's mightiest heroes. Like Kevin Bacon.",
  "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
  "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
  "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
  "direction": "outbound-api",
  "error_code": null,
  "error_message": null,
  "from": "+14155552345",
  "messaging_service_sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "num_media": "0",
  "num_segments": "1",
  "price": null,
  "price_unit": null,
  "sid": "MMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "status": "sent",
  "subresource_uris": {
    "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
  },
  "to": "+15558675310",
  "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
}

'''