import socket
import json
import session


class CreateRoomAuction:
    def __init__(self,server_socket):
        self.server_socket = server_socket
        self.dict = session.session
        
    def sendDataCreateRoom(self):
        msg = f"CREATEROOM {self.dict['idUser']} {self.nameRoom}"
        self.server_socket.sendall(bytes(msg, "utf8"))

    def receiDataCreateRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', dataRec)
        data = dataRec.split(" ")
        if data[0] == "CREATEROOM":
            print("Create room success!")
        else:
            print("Create room fail!")
            
        return data[1], data[2], data[3]


    def createRoom(self):
        self.nameRoom = input("Tên Phòng: ")
        self.sendDataCreateRoom()
        return self.receiDataCreateRoom()
    