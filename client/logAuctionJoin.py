import session

class LogAuction:
    
    dict = session.session

    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.dict = LogAuction.dict

    def sendDataLogAuction(self):
        msg = f"LOGAUCTION {self.dict['idUser']}"
        self.server_socket.sendall(bytes(msg, "utf8"))

    def receiDataLogAuction(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
    
        print('Server: ', dataRec)
        data = dataRec.split(" ")
        data.remove("LOGAUCTION")
        print("\n\tID\tTên Phòng")
        for item in data:
            idRoom, nameRoom = item.split(",")
            print("\n{} \t{}".format(idRoom, nameRoom))
        

    def outputScreen(self):
        print("Danh sách phòng đấu giá đã tham gia")
        self.receiDataLogAuction()

    def logAuctionJoin(self):
        self.sendDataLogAuction()
        self.outputScreen()


        