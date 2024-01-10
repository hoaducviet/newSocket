import session

class LogUser:
    
    dict = session.session

    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.dict = LogUser.dict

    def sendDataLogProduct(self):
        msg = f"LOGPRODUCT {self.dict['idUser']}"
        self.server_socket.sendall(bytes(msg, "utf8"))

    def receiDataLogProduct(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
    
        print('Server: ', dataRec)
        data = dataRec.split(" ")
        data.remove("LOGPRODUCT")
        print("\n\tID\tTên Sản Phẩm")
        for item in data:
            idProduct, nameProduct = item.split(",")
            print("\n{} \t{}".format(idProduct, nameProduct))
        

    def outputScreen(self):
        print("Danh sách vật phẩm đã mua")
        self.receiDataLogProduct()

    def logProductBuy(self):
        self.sendDataLogProduct()
        self.outputScreen()


        