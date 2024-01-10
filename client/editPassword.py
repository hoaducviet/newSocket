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
        data = self.server_socket.recv(1024).decode("utf8")
        print('Server: ', data)

    def editPassword(self):
        newpassword = input("Nhập mật khẩu mới: ")
        self.sendDataEditPassword(newpassword)
        self.receiDataEditPassword()