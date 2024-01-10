import session

class ProductAuction:
    def __init__(self,server_socket,stateProduct):
        self.server_socket = server_socket
        self.dict = session.session
        self.dictRoom = []
        self.index = 0
        self.stateProduct = stateProduct
        self.numberRoom = 0

    def sendDataMyRoom(self):
        msg = f"{self.stateProduct}"
        self.server_socket.sendall(bytes(msg, "utf8"))


    def receiDataMyRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        #dataRec = "PRODUCTAUCTING iduser idProduct1,nameProduct1,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
        print('Server: ', dataRec)
        data = dataRec.split(" ")

        print("\nSTT\tIDProduct\tNameProduct\tIDRoom\tNameRoom")
        for item in data[2:]:
            product = item.split(",")
            self.index += 1
            print(f"\n{self.index}\t{product[0]}\t{product[1]}\t{product[2]}\t{product[3]}")
            self.dictRoom.append({
                "idRoom": product[2],
                "nameRoom": product[3]
            })

    def option(self):
        pass
        while True:
            case = int(input("Chọn vật phẩm đề xem phòng (Nhập O để quay lại): "))
            if case == 0:
                break
            elif case > self.index:
                print("\nKhông có vật phẩm đã chọn")
                break
            else:
                print(f"\nXem phòng chứa vật phẩm số {case}")
                self.numberRoom =  case
                break

    def productAuction(self):
        self.sendDataMyRoom()
        self.receiDataMyRoom()
        self.option()
        return [self.dictRoom[self.numberRoom-1]['idRoom'], self.dictRoom[self.numberRoom-1]['nameRoom']]
        
# user = ProductAuction(1).productAuction()
# print(user)