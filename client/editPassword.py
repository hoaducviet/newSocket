import session

class EditPassword:
    def __init__(self,server_socket, role = 0):
        self.server_socket = server_socket
        self.dict = session.session
        self.role = role
        
    def sendDataEditPassword(self, newpassword):
        msg = f"EDITUSERPASSWORD {self.dict['idUser']} {newpassword}"
        self.server_socket.sendall(bytes(msg, "utf8"))

    def receiDataEditPassword(self):
        dataR = self.server_socket.recv(1024).decode("utf8")
        data = dataR.split(" ")
        if data[0] == "EDITUSERPASSWORD":
            print("Edit password success!")
        else:
            print("Edit password fail!")

    def editPassword(self):
        newpassword = input("Nhập mật khẩu mới: ")
        self.sendDataEditPassword(newpassword)
        self.receiDataEditPassword()