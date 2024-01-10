import socket
import json
import session


class RemoveProductRoomAuction:
    def __init__(self,server_socket,idRoom):
        self.server_socket = server_socket
        self.dict = session.session
        self.idRoom = idRoom
        self.list = []
        self.listIdProductRemove = []
        self.index = 0
        
    

    def sendDataGetProductRoom(self):
        msg = f"VIEWPRODUCTROOM {self.dict['idUser']} {self.idRoom}"
        self.server_socket.sendall(bytes(msg, "utf8"))


    def receiDataGetProductRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', dataRec)
        data = dataRec.split(" ")

        print("\nDanh Sách Vật Phẩm\nSTT\tName\tDescribe\tStart Price\tTime Auction")
        for item in data[3:]:
            product = item.split(",")
            self.list.append({
                "idProduct": product[0],
                "nameProduct": product[1],
                "describeProduct": product[2],
                "startPrice": product[3],
                "timeAuction": product[4]
            })
            self.index += 1
            print(f"\n{self.index}\t{product[0]}\t{product[1]}\t{product[2]}\t{product[3]}\t{product[4]}")



    def sendDataRemoveProductRoom(self):
        msg = f"REMOVEPRODUCTROOM {self.dict['idUser']} {self.idRoom}"
        for item in self.listIdProductRemove:
            msg += f" {item}"
            self.server_socket.sendall(bytes(msg, "utf8"))
        
            

    def receiDataRemoveProductRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', dataRec)

    def option(self):
        while True:
            case = int(input("Chọn vật phẩm cần xoá (Nhập O để quay lại): "))
            if case == 0:
                break

            elif case > self.index:
                print("\nKhông có vật phẩm phù hợp")
                break
            else:
                if self.list[case-1]["idProduct"] not in self.listIdProductRemove:
                    self.listIdProductRemove.append(self.list[case-1]["idProduct"])
                break

    def listProductRoom(self):
        while True:
            print("\n1.Xoá thêm 1 vật phẩm\n2.Lưu")
            case = int(input("Lựa chọn: "))
            if case == 1:
                self.option()
                print(self.listIdProductRemove)
                
            elif case == 2:
                break
    
    def removeProductRoomAuction(self):
        self.sendDataGetProductRoom()
        self.receiDataGetProductRoom()
        self.listProductRoom()
        self.sendDataRemoveProductRoom()
        self.receiDataRemoveProductRoom()


