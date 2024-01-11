import socket
import json
import session


class AddProductRoomAuction:
    def __init__(self,server_socket,idRoom):
        self.server_socket = server_socket
        self.dict = session.session
        self.idRoom = idRoom
        self.list = []
        #self.list = [{'nameProduct': 'oto', 'describeProduct': 'dfasdfasd', 'startPrice': 123.0, 'timeAuction': 123.0}, {'nameProduct': 'viet', 'describeProduct': 'afsdfasdf', 'startPrice': 12.0, 'timeAuction': 43.0}]
        


    def addProduct(self):
        product = {}
        product['nameProduct'] = input("\nTên sản phẩm: ")
        product['describeProduct'] = input("\nMô tả: ")
        product['startPrice'] = float(input("\nGiá khởi điểm ($): "))
        product['timeAuction'] = float(input("\nThời gian bán đấu giá (h)): "))
        return product

    def listProductRoom(self):
        while True:
            print("\n1.Thêm 1 vật phẩm\n2.Lưu")
            case = int(input("Lựa chọn: "))
            if case == 1:
                self.list.append(self.addProduct())
                print (self.list)
            elif case == 2:
                break
            
    def sendDataAddProductRoom(self):
        msg = f"ADDPRODUCTROOM {self.dict['idUser']} {self.idRoom}"
        for item in self.list:
            msg += " {},{},{},{}".format(item['nameProduct'],item['describeProduct'],item['startPrice'],item['timeAuction'])
        
        self.server_socket.sendall(bytes(msg, "utf8"))

    def receiDataAddProductRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        data = dataRec.split(",")
        if data[0] == "ADDPRODUCTROOM":
            print("Add product success!")

        else:
            print("Add product fail")

    def addProductRoomAuction(self):
        self.listProductRoom()
        if len(self.list) > 0:
            self.sendDataAddProductRoom()
            self.receiDataAddProductRoom()

