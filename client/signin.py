import json

class SignIn:
    def __init__(self,server_socket):
        self.server_socket = server_socket
        self.dict = {}
    def inputData(self):
        print("\nĐăng Nhập\n")
        self.username = input("UserName: ")
        self.password = input("Password: ")

    def sendDataUser(self):
        msg = f"SIGNIN {self.username} {self.password}"
        self.server_socket.sendall(bytes(msg, "utf8"))


    def receiData(self):
        print("\nDone Sign In")
        dataRec = self.server_socket.recv(1024).decode("utf8")
        
        print('Server: ', dataRec)
    
        data = dataRec.split(" ")
        if data[0] == "SIGNIN":
            self.dict = {
                "idUser" : "{}".format(data[1]),
                "userName" : "{}".format(data[2]),
            }

        with open("session.json","w") as file:
            json.dump(self.dict, file, indent=4)

    def signIn(self):
        self.inputData()
        self.sendDataUser()
        self.receiData()
