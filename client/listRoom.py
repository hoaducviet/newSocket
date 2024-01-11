import session

class ListRoom:
    def __init__(self,server_socket, role = 0):
        self.server_socket = server_socket
        self.dict = session.session
        self.role = role
        self.dictRoom = []
        self.index = 0
        self.numberRoom = 0

    def sendDataMyRoom(self):
        if self.role:
            msg = f"LISTMYROOM {self.dict['idUser']}"
        else:
            msg = f"LISTROOM {self.dict['idUser']}"
        
        self.server_socket.sendall(bytes(msg, "utf8"))
        print(msg)

    def receiDataMyRoom(self):
        dataRec = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', dataRec)
        data = dataRec.split(" ")

        if len(data) == 2:
            print("\nNo data room")
        elif len(data) > 2:

            print("\nDanh Sách Phòng\nSTT\tIDRoom\t\tNameRoom")
            for item in data[2:]:
                product = item.split(",")
                self.index += 1
                print(f"\n{self.index}\t{product[0]}\t{product[1]}")
                self.dictRoom.append({
                    "idRoom": product[0],
                    "nameRoom": product[1]
                })
        else:
            print("Error!")


    def option(self):
        while True:
            case = int(input("Chọn phòng: "))
            if case > self.index or case <= 0:
                print("\nKhông có phòng đã chọn")
            else:
                self.numberRoom = case
                break

    def listRoom(self):
        self.sendDataMyRoom()
        self.receiDataMyRoom()
        self.option()
        return [self.dictRoom[self.numberRoom-1]['idRoom'], self.dictRoom[self.numberRoom-1]['nameRoom'], self.role]
        
     