# IMPORT --------------------------------------------------------------
# Utility
import socket
import logging
import time
import threading
import datetime
# Azure Table
from os import pipe
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

# Variables
global UDP_IP
global UDP_PORT

UDP_IP = "192.168.100.20"
UDP_PORT = 54120




class alive_to_Lox(object):
    def __init__(self):
        pass

    def start(self, sock):
        aliveCount = 0
        while True:
            # Controll Message to Loxone
            message = 'AliveAzureTableBridge' + str(aliveCount)
            sock.sendto(str.encode(message), (UDP_IP, UDP_PORT))
            aliveCount += 1
            if aliveCount > 1:
                aliveCount = 0
            time.sleep(5)

class loxMessagetoAzureTabel(object):
    TABLE_STROMBEZUG = "Strombezug"
    def __init__(self):
        credential = "eFH0EUaE6HU8GaqS9S04vf2MLdQ94vMdbMg6kaMetKG1gXU8g+QUtfAKxbtvyjj6Vrq4X3E0hBVNe5gIzjFZHQ=="
        self.table_service = TableService(account_name="jofustrom456789", account_key=credential)

    def send_newMessage_to_Azure(self, msg):
        now = datetime.datetime.now()
        msg = str(msg)
        msg = msg[2:-1]
        data = msg.split("$")
        PartitionKey = data[0]
        if now.month == 1:
            y = now.year -1
            last_month = 12
        else:
            y = now.year
            last_month = now.month-1

        f = "PartitionKey eq '" + str(PartitionKey) + "' and year eq " + str(y) + " and month eq " + str(last_month) + " and tarif eq '" + str(data[1]) + "'"
        print(f)
        existing_entity = self.table_service.query_entities(self.TABLE_STROMBEZUG, filter=f , timeout=60)
        existing_entity = list(existing_entity)

        if (len(existing_entity) == 0):
                entity = Entity()
                entity.PartitionKey = PartitionKey
                entity.RowKey = str(100000000000000 - round(time.time()) )
                entity.tarif = data[1]
                entity.year = y
                entity.month = last_month
                entity.value = data[2]
                entity.unit = data[3]
                entity.paid = False
                entity.cleared = False
                self.table_service.insert_entity(self.TABLE_STROMBEZUG, entity)


class recive_datafromLox(object):
    def __init__(self):
        self.lmat = loxMessagetoAzureTabel()
        pass

    def start(self, sock):
        print("service startet")
        try:
            while True:
                msg, addr = sock.recvfrom(
                    1024)  # buffer size is 1024 bytes
                #logging.debug("received message:" + str(data))
                print("received message:" + str(msg))
                self.lmat.send_newMessage_to_Azure(msg)

        except KeyboardInterrupt:
            print("Press Ctrl-C to terminate while statement")
            pass


def main():

    logging.info("service startet")
    
    # Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(("", UDP_PORT))

    rcv = recive_datafromLox()
    send = alive_to_Lox()
    t1 = threading.Thread(target=rcv.start, args=(sock, ))
    t2 = threading.Thread(target=send.start, args=(sock,))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        pass

if __name__ == '__main__':
    main()
    print("end")
