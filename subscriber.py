import paho.mqtt.client as paho
import sqlite3
from sqlitehandler import write_to_db
#from mongohandler import write_to_db

def on_message(mosq, obj, msg):
    print ("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))
    write_to_db(msg.topic, msg.payload)
    mosq.publish('pong', 'ack', 0)

def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':
    broker = "127.0.0.1"
    port = 1883
    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    # Not working with certificates yet!
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883)

    client.subscribe("table_Terrazatemperatura/#", 0)
    client.subscribe("table_Patiotemperatura/#", 0)
    client.subscribe("table_Jardintemperatura/#", 0)

    while client.loop() == 0:
        pass

####                                                                             ####
#                                                                                   #
# HINT: When writing to db replace the "/" in the topic names with for example "_", #
#       as sqlite doesn't support "/" in table's names                              #
#                                                                                   #
####                                                                             ####
