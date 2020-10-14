# IMPORT --------------------------------------------------------------
# Utility
import socket
import logging
import time
import threading
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
    def __init__(self):
        credential = "eFH0EUaE6HU8GaqS9S04vf2MLdQ94vMdbMg6kaMetKG1gXU8g+QUtfAKxbtvyjj6Vrq4X3E0hBVNe5gIzjFZHQ=="
        self.table_service = TableService(account_name="jofustrom456789", account_key=credential)

    def send_newMessage_to_Azure(self, msg):
        msg = str(msg)
        msg = msg[2:-1]
        data = msg.split("$")
        entity = Entity()
        entity.PartitionKey = data[0]
        entity.RowKey = str(100000000000000 - round(time.time()) )
        entity.value = data[1]
        entity.unit = data[2]
        entity.paid = False
        entity.cleared = False
        self.table_service.insert_entity('D41Strombezug', entity)


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
