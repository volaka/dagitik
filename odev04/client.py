#!/usr/bin/env python
import socket
import threading


class readThread(threading.Thread):
    def __init__(self, servSock):
        threading.Thread.__init__(self)
        self.s = servSock

    def run(self):
        try:
            while not Stop:
                rec = self.s.recv(1024)
                print "Server:", rec
        except Exception, Argument:
            print Argument


class writeThread(threading.Thread):
    def __init__(self, servSock, inp):
        threading.Thread.__init__(self)
        self.s = servSock
        self.inp = inp

    def run(self):
        try:
            self.s.sendall(inp)
        except Exception, Argument:
            print Argument


Stop = False
try:
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))

    rThread = readThread(s)
    rThread.start()
    print "To Exit, enter 'eof'"
    while True:
        inp = raw_input(">>")
        wThread = writeThread(s, inp)
        wThread.start()
        if inp.lower() == "eof":
            Stop = True
            break

except KeyboardInterrupt:
    print "Keyboard Interrupt"
except Exception:
    print "Hata Main"
finally:
    s.close()
    rThread.join()
    print "Read Thread Finished"
print "Exiting"
