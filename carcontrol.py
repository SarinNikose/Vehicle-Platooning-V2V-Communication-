import bluetooth
import time
import socket
import RPi.GPIO as GPIO

HOST = "192.168.43.236"
PORT = 5468

m11=23
m12=24
m21=16
m22=20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM ) 
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
 
client_socket,address = server_socket.accept()
print ("Accepted connection from ",address)

def left_side_forward():
    print( "FORWARD LEFT")
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    time.sleep(1)
    print("Done1")
    GPIO.output(m11 , 1)
    GPIO.output(m12 , 0)
    print("Done2")
def right_side_forward():
   print ("FORWARD RIGHT")
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   time.sleep(.5)
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)

def forward():
   print ("FORWARD")
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)

def left_side_reverse():
   print ("BACKWARD LEFT")
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   time.sleep(.5)
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)

def right_side_reverse():
   print ("BACKWARD RIGHT")

   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   time.sleep(.5)
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)

def reverse():
   print ("BACKWARD")
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)

def stop():
   print ("STOP")
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)


def send(sendata):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    #host  = socket.gethostname()
    #print(host)
    #while True:
    s.sendto(str.encode(sendata),(HOST,PORT))
    print(sendata)
    time.sleep(1)
   
 
data=""
while 1:
         data= client_socket.recv(1024)
         print(data)
         #data = list(data)[2]
         #data = str(data)
         data = data.decode("utf-8")
         print ("Received: %s" % data)
         #data = "R"
         if (data == "F"):    
            forward()
            send(data)
         elif (data == "L"):    
            left_side_forward()
            send(data)
         elif (data == "R"):    
            right_side_forward()
            send(data)
         elif (data == "B"):    
            reverse()
            send(data)
         elif (data == "A"):    
            left_side_reverse()
            send(data)
         elif (data == "P"):    
            right_side_reverse()
            send(data)
         elif data == "S":
            stop()
            send(data)
         elif (data == "Q"):
            send("Quit")
            print ("Quit")
            break
client_socket.close()
server_socket.close()
