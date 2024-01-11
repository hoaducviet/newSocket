import socket
import json
import threading

HOST = '127.0.0.1'  
PORT = 8000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)


userIndex = 0

def handle_client(client, addr):
    global userIndex

    try:
        print('Connected by', addr)
        while True:
            data = client.recv(1024)
            if not data:
                print("Client disconnected: ", addr)
                break

            str_data = data.decode("utf8")
            dataR = str_data.split(" ")
            if str_data == "quit":
                break
            
            
            msg = ""
            if dataR[0] == "SIGNIN":
                msg = ""
                with open("userAccount.json","r") as f:
                    userList = json.load(f)

                for item in userList:
                    if dataR[1] == item["username"] and dataR[2] == item["password"]:
                        msg += f"SIGNIN {item['idUser']} {item['username']}"
                        break
                else:
                    msg += "Error"

            if dataR[0] == "SIGNUP":
                msg = ""
                userList = []
                with open("userAccount.json","r") as f:
                    userList = json.load(f)
                if dataR[1] in userList:
                    msg += "Error"
                else:
                    userIndex += 1
                
                    idUser = f"user-{userIndex}-{dataR[1]}"
                    userList.append({
                        "idUser": idUser,
                        "username": dataR[1],
                        "password": dataR[2],
                        "email": dataR[3],
                    })
                    with open("userAccount.json","w") as f:
                        json.dump(userList, f, indent = 4)

                    msg += f"SIGNUP {idUser} {dataR[1]}"


            if dataR[0] == "EDITUSERPASSWORD":
                msg = ""
                userList = []
                with open("userAccount.json","r") as f:
                    userList = json.load(f)
                
                idx = 0
                check = False
                for item in userList:
                    idx += 1
                    if dataR[1] == item["idUser"]:

                        msg += f"EDITUSERPASSWORD {item['idUser']}"
                        userList[idx-1]['password'] = dataR[2]
                        with open("userAccount.json","w") as f:
                            json.dump(userList, f, indent = 4)
                        check = True
                        break
                if not check:
                    msg += "Error"

                #msg += "EDITUSERPASSWORD iduser Change,password,successed"



            if dataR[0] == "LOGPRODUCT":
                msg += "LOGPRODUCT idProduct1,nameProduct1 idProduct2,nameProduct2"
            if dataR[0] == "LOGAUCTION":
                msg += "LOGAUCTION idRoom1,nameRoom1 idRoom2,nameRoom2"
            if dataR[0] == "CREATEROOM":
                msg += "CREATEROOM idUser idRoom nameRoom"
            if dataR[0] == "DELETEROOM":
                msg += "DELETEROOM idUser idRoom nameRoom deleted"
            if dataR[0] == "ADDPRODUCTROOM":
                msg += "Add product successed"
            if dataR[0] == "VIEWPRODUCTROOM":
                msg += "VIEWPRODUCTROOM iduser idRoom idProduct1,oto,dfasdfasd,123.0,123.0 idproduct2,viet,afsdfasdf,12.0,43.0 idProduct3,viet,hoangasdf,12.0,123.0"
            if dataR[0] == "REMOVEPRODUCTROOM":
                msg += "REMOVEPRODUCTROOM iduser idRoom removeok"
            if dataR[0] == "LISTMYROOM":
                msg += "LISTMYROOM iduser idRoom1,nameRoom1 idRoom2,nameRoom2"
            if dataR[0] == "LISTROOM":
                msg += "LISTROOM iduser idRoom3,nameRoom3 idRoom4,nameRoom4"
            if dataR[0] == "PRODUCTAUCTIONED":
                msg += "PRODUCTAUCTIONED iduser idProduct1,nameProduct1,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "PRODUCTAUCTING":
                msg += "PRODUCTAUCTING iduser idProduct3,nameProduct3,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "PRODUCTAUCTION":
                msg += "PRODUCTAUCTION iduser idProduct4,nameProduct4,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "SEARCHPRODUCTINFOR":
                msg += "SEARCHPRODUCTINFOR iduser idProduct1,nameProduct1,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "SEARCHPRODUCTTIME":
                msg += "SEARCHPRODUCTTIME iduser idProduct3,nameProduct3,idRoom3,nameRoom3 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "VIEWROOM":
                msg += "VIEWROOM iduser idRoom nameRoom idProduct nameProduct nowPrice buyNowPrice time"
            

            if dataR[0] == "BUYNOW":
                msg += "BUYNOW Buysuccessed!"

            if dataR[0] == "BIDPRICE":
                msg += "BIDPRICE iduser idRoom idProduct newPrice time"
            
            if dataR[0] == "LOGROOM":
                msg += "LOGROOM idRoom idProduct1,nameProduct1,idUser1,userName1,price1,time1 idProduct2,nameProduct2,idUser2,userName2,price2,time2"
            
        
            
            print("Client port{}: ".format(addr) + str_data)
            #print(msg)
            #msg = input("Server: ")
            print("Server: " + msg)
            client.sendall(bytes(msg, "utf8"))
                
    finally:
        client.close()


      

while True:
    client, addr = s.accept()
    client_thread = threading.Thread(target=handle_client, args=(client, addr))
    client_thread.start()
    
s.close()