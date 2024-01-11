import json
import session


class RemoveRoomAuction:
    def __init__(self,server_socket,idRoom):
        self.server_socket = server_socket
        self.idRoom = idRoom
        self.idUser = session.session['idUser']

    def sendDataUser(self):
        msg = f"DELETEROOM {self.idUser} {self.idRoom}"
        self.server_socket.sendall(bytes(msg, "utf8"))

    def receiData(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        data = dataRec.split(" ")
        print('Server: ', dataRec)
        
        if data[0] == "DELETEROOM":
            print("Delete room success!")
        else: 
            print("Delete room fail!")
            
    def removeRoom(self):
        self.sendDataUser()
        self.receiData()
