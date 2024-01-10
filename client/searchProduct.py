import session

class SearchProduct:
    def __init__(self,server_socket):
        self.server_socket = server_socket
        self.dict = session.session
        self.dictRoom = []
        self.index = 0
        self.inputSearchTime = ""
        self.inputSearchInfor = ""
        self.caseRoom = 0
        

    def sendDataSearchProduct(self,option):

        if option == "infor":
            msg = f"SEARCHPRODUCTINFOR {self.dict['idUser']} {self.inputSearchInfor}"
        if option == "time":
            msg = f"SEARCHPRODUCTTIME {self.dict['idUser']} {self.inputSearchTime}"
        self.server_socket.sendall(bytes(msg, "utf8"))
        print(msg)

    def receiDataSearchProduct(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', dataRec)
        data = dataRec.split(" ")

        print("\nSTT\tIDProducut\tNameProduct\tIDRoom\tNameRoom")
        for item in data[2:]:
            product = item.split(",")
            self.index += 1
            print(f"\n{self.index}\t{product[0]}\t{product[1]}\t{product[2]}\t{product[3]}")
            self.dictRoom.append({
                "idRoom": product[2],
                "nameRoom": product[3]
            })

    def option(self):
        while True:
            caseRoom = int(input("Chọn phòng (Nhập O để quay lại): "))
            if caseRoom == 0:
                break

            elif caseRoom > self.index:
                print("\nKhông có phòng đã chọn")
                break
            else:
                print(f"\nĐang xem phòng số {caseRoom}")
                self.caseRoom = caseRoom
                break

    def searchProduct(self):
        while True:
            print("\n1.Tìm theo khung giờ\n2.Tìm theo tên vật phẩm\n3.Trở lại")
            case = int(input("Lựa chọn: "))

            if case == 1:
                self.inputSearchTime += input("Nhập vào thời gian tìm kiếm: ")
                self.sendDataSearchProduct("time")
                self.receiDataSearchProduct()
                self.option()
                break
            elif case == 2:
                self.inputSearchInfor += input("Nhập vào tên sản phẩm tìm kiếm: ")
                self.sendDataSearchProduct("infor")
                self.receiDataSearchProduct()
                self.option()
                break
            elif case == 3:
                break
            else:
                print("\nVui lòng chọn lại")

        return [self.dictRoom[self.caseRoom-1]['idRoom'], self.dictRoom[self.caseRoom-1]['nameRoom']]
 