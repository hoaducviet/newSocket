import session

class ViewRoom:
    def __init__(self,server_socket,idRoom):
        self.server_socket = server_socket
        self.dict = session.session
        self.idRoom = idRoom
        
    
    def sendDataLogRoom(self):
        msg = f"LOGROOM {self.idRoom}"
        self.server_socket.sendall(bytes(msg, "utf8"))
        print(msg)

    def receiDataLogRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        #dataRec = "LOGROOM idRoom idProduct1,nameProduct1,idUser1,userName1,price1,time1 idProduct2,nameProduct2,idUser2,userName2,price2,time2"
        print('Server: ', dataRec)

        data = dataRec.split(" ")
        print("\nIdProduct\tName Product\tIdUser\tuserName\tPrice\tTime")
        for item in data[2:]:
            log = item.split(",")
            print(f"\n{log[0]}\t{log[1]}\t{log[2]}\t{log[3]}\t{log[4]}\t{log[5]}")
        

    def sendDataBidPriceProduct(self):
        price = float(input("Ra giá: "))
        msg = f"BIDPRICE {self.idRoom} {self.data[4]} {price}"
        self.server_socket.sendall(bytes(msg, "utf8"))
        print(msg)

    def receiDataBidPriceProduct(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        #dataRec = "BIDPRICE iduser idRoom idProduct newPrice time"
       

        data = dataRec.split(" ")
        if data[0] == "BIDPRICE":
            self.data[6],self.data[8] = data[4],data[5]
            print("\nĐã được đặt giá mới")
        else:
            print("\nKhông hợp lệ")


    def sendDataBuyNowdPriceProduct(self):
        msg = f"BUYNOW {self.idRoom} {self.data[7]}"
        self.server_socket.sendall(bytes(msg, "utf8"))
        

    def receiDataBuyNowPriceProduct(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        if dataRec == "BUYNOW":
            print("\nĐã được mua")

        
    

    def logRoom(self):
        self.sendDataLogRoom()
        self.receiDataLogRoom()

    def bidPriceProduct(self):
        self.sendDataBidPriceProduct()
        self.receiDataBidPriceProduct()


    def buyNowPriceProduct(self):
        self.sendDataBuyNowdPriceProduct()
        self.receiDataBuyNowPriceProduct()


    def sendDataViewRoom(self):
        msg = f"VIEWROOM {self.idRoom}"
        self.server_socket.sendall(bytes(msg, "utf8"))
        
        

    def receiDataViewRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        self.data = dataRec.split(" ")

    def output(self):

        print(f"\nTên Phòng: {self.data[3]}\nSản phẩm đang đấu giá: {self.data[5]}\nGiá hiện tại: {self.data[6]}\nGiá bán trực tiếp: {self.data[7]}\nThời gian còn lại: {self.data[8]}")

    def screenAuction(self):
        self.sendDataViewRoom()
        self.receiDataViewRoom()

        while True:
            self.output()
            print("\nĐấu Giá\n1.Tố giá\n2.Mua trực tiếp\n3.Lịch sử của phiên\n4.Thoát")
            case = int(input("Lựa chọn: "))
            if case == 1:
                print("\nTố giá")
                self.bidPriceProduct()

            elif case == 2:
                print("\nMua trực tiếp")
                self.buyNowPriceProduct()
                break

            elif case == 3:
                print("Lịch sử của phiên")
                self.logRoom()

            elif case == 4:
                break

    def viewRoom(self):
        self.screenAuction()

