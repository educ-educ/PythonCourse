#!/usr/bin/env python
import pika, sys
import time
import json
import os
from flask import Flask, jsonify, request


def main():
    # Подключился к серверу на локальном компьютере
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # channel = connection.channel()


    # hostname = 'amqp://hljhaczs:J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J@toad.rmq.cloudamqp.com/TestGoConsumer?exchange:TestGoConsumer'
    # connection = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=hostname))
    # channel = connection.channel()

    #url = os.environ.get('CLOUDAMQP_URL', 'amqp://hljhaczs:J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J@toad.rmq.cloudamqp.com/TestGoConsumer?exchange:TestGoConsumer')
    credentials = pika.PlainCredentials('hljhaczs', 'J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J')
    params = pika.URLParameters('amqps://hljhaczs:J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J@toad.rmq.cloudamqp.com/hljhaczs/GetRoles?exchange:GetRoles')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()


    channel.queue_declare(queue='GetRoles', durable=True)

    # hostname = 'localhost'
    # crecredentials = pika.PlainCredentials('admin@mail.ru','Admin_123')
    # r = 'hljhaczs:J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J'
    # crecredentials = pika.PlainCredentials('hljhaczs', 'J5W5ouprR8fKEkmGKvpmd0ijcs3BbX8J')

    #callback-функция для получения сообщений из очереди
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # получение сообщений из указанной очереди
    channel.basic_consume(queue='GetRoles', on_message_callback=callback, auto_ack=True)

    # уверяемся, что очередь существует. Очередь с одним названием может быть создана только раз
    """
    durable - долговечная очередь 
    """
    #channel.queue_declare(queue='hello')
    #channel.queue_declare(queue='task_queue', durable=True)

    # определяем тип exchang'а как разветляющийся (fanout)
    # channel.exchange_declare(exchange='logs', exchange_type='fanout')


    # тип обменника direct
    #channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    #result = channel.queue_declare(queue='', exclusive=True)
    #queue_name = result.method.queue

    # severities = sys.argv[1:]
    # if not severities:
    #     sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    #     sys.exit(1)
    #
    # for severity in severities:
    #     channel.queue_bind(
    #         exchange='direct_logs', queue=queue_name, routing_key=severity)
    #
    # print(' [*] Waiting for logs. To exit press CTRL+C')
    #
    # def callback(ch, method, properties, body):
    #     print(" [x] %r:%r" % (method.routing_key, body))



    # пустое имя очереди --> случайное, exclusive = удаление очереди при отключении consumer'а
    # result = channel.queue_declare(queue='', exclusive=True)
    # queue_name = result.method.queue

    """
        binding -  relationship between exchange and a queue
    """
    #channel.queue_bind(exchange='logs', queue=queue_name)
    # теперь обменник будет помещать сообщения в очередь
    """
    сохранение логов
    python receive_logs.py > logs_from_rabbit.log
    python receive.py
    python send.py
    """


    # channel.basic_publish(exchange='logs',
    #                       routing_key='',
    #                       body=message)

    # callback-функция для получения сообщений из очереди
    # def callback(ch, method, properties, body):
    #     print(" [x] Received %r" % body)

    # функция, симулирующая процесс работы, зависает на [кол-во точек в сообщении] секунд
    '''def fake_work_callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)'''

    # получение сообщений из указанной очереди
    # channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # получение сообщений из указанной очереди
    """
    auto_ack - автоподтверждение получения сообщения
    """

    #channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    #channel.basic_consume(queue='hello', on_message_callback=fake_work_callback)
    # channel.basic_qos(prefetch_count=1)
    # channel.basic_consume(queue='task_queue', on_message_callback=callback)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)