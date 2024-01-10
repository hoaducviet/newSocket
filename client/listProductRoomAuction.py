import socket
import json
import session

class ListProductRoomAuction:
    def __init__(self,server_socket,idRoom):
        self.server_socket = server_socket
        self.dict = session.session
        self.idRoom = idRoom
        
    def sendDataListProductRoom(self):
        msg = f"VIEWPRODUCTROOM {self.dict['idUser']} {self.idRoom}"
        self.server_socket.sendall(bytes(msg, "utf8"))
        print(msg)

    def receiDataListProductRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', dataRec)
        data = dataRec.split(" ")

        print("\nDanh Sách Vật Phẩm\nIDProduct\tName\tDescribe\tStart Price\tTime Auction")
        for item in data[3:]:
            product = item.split(",")
            print(f"\n{product[0]}\t{product[1]}\t{product[2]}\t{product[3]}\t{product[4]}")
    

    def viewProductRoom(self):
        self.sendDataListProductRoom()
        self.receiDataListProductRoom()
        

            