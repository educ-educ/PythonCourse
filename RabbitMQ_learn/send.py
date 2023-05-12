#!/usr/bin/env python
import pika
import sys
import json
import os
from flask import Flask, jsonify, request

# Подключился к серверу на локальном компьютере
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# hostname = "amqps://hljhaczs:J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J@toad.rmq.cloudamqp.com/hljhaczs"
# #hostname = 'localhost'
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
# channel = connection.channel()

credentials = pika.PlainCredentials('hljhaczs', 'J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J')
params = pika.URLParameters('amqps://hljhaczs:J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J@toad.rmq.cloudamqp.com/hljhaczs/EditUser?exchange:EditUser')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='nikita')


m = {"properties":{'contentType': 'application/json'},
     "reply_to": 'nikita',
     "payload":{{'id':'451921', 'Password':'Admin_123'}
                }
     }

js = json.dumps(m)
channel.basic_publish(exchange='', routing_key='hello', body=js)
connection.close()

'''
# Создал очередь с названием 'hello'
channel.queue_declare(queue='hello')
# Создал долговечную очередь с названием 'task_queue'
channel.queue_declare(queue='task_queue', durable=True)

# создал обменник типа fanout (разветвление)
# routing_key игнорируется в таком типе обменников
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# обменник типа direct
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()

# Отправка в очередь
"""
exchange - обменник
routing_key - название очереди
body - сообщение
"""
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')
# print(" [x] Sent 'Hello World!'")


message = ' '.join(sys.argv[1:]) or "Hello World!"

# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body=message)

# channel.basic_publish(exchange='',
#                       routing_key="task_queue",
#                       body=message,
#                       properties=pika.BasicProperties(
#                          delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
#                       ))


# channel.basic_publish(exchange='logs', routing_key='', body=message)

# print(" [x] Sent %r" % message)
# отключиться от сервера
connection.close()

'''
