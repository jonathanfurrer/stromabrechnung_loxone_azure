import socket
import logging
import time
import threading

# Variables
global UDP_IP
global UDP_PORT

UDP_IP = "192.168.100.20"
UDP_PORT = 54120

# Config logging
# logging.basicConfig(filename="/home/pi/git/unifi_loxone_bridge/log.log",
logging.basicConfig(filename="c:/log.log",
                    level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)


class alive_to_Lox(object):

    def __init__(self):
        pass

    def start(self, sock):
        aliveCount = 0
        while True:
            # Controll Message to Loxone
            message = 'AliveFromPowerMeter' + str(aliveCount)
            sock.sendto(str.encode(message), (UDP_IP, UDP_PORT))
            aliveCount += 1
            if aliveCount > 1:
                aliveCount = 0
            time.sleep(5)


class recive_datafromLox(object):
    def __init__(self):
        pass

    def start(self, sock):

        try:
            while True:
                data, addr = sock.recvfrom(
                    1024)  # buffer size is 1024 bytes
                logging.debug("received message:" + str(data))

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
