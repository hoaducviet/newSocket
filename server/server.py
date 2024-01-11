import socket
import json
import threading

HOST = '127.0.0.1'  
PORT = 8001


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)


userIndex = 0
roomIndex = 0
productIndex = 0
time = 60
def handle_client(client, addr):
    global userIndex
    global roomIndex
    global productIndex
    global time
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

            if dataR[0] == "LOGPRODUCT":
                msg += "LOGPRODUCT room-0-nam-0,tauthuy room-0-nam,xetang"
            if dataR[0] == "LOGAUCTION":
                msg += "LOGAUCTION room-0-viet,viet room-0-noname,noname room-0-nam,nam"


            if dataR[0] == "CREATEROOM":
                roomList = []
                msg = ""
                with open("room.json","r") as f:
                    roomList = json.load(f)

                for item in roomList:
                    if dataR[1] == item['idRoom']:
                        msg += "Error"
                    break
                    
                idUser = f"user-{userIndex}-{dataR[1]}"
                newRoom = {
                    "idUser": dataR[1],
                    "idRoom": f"room-{roomIndex}-{dataR[2]}",
                    "nameRoom": dataR[2],
                }
                roomList.append(newRoom)
                with open("room.json","w") as f:
                    json.dump(roomList, f, indent = 4)

                msg += f"CREATEROOM {newRoom['idUser']} {newRoom['idRoom']} {newRoom['nameRoom']}"


                

            if dataR[0] == "DELETEROOM":
                roomList = []
                msg = ""
                with open("room.json","r") as f:
                    roomList = json.load(f)
                check = 0
                for item in roomList:
                    if dataR[2] == item['idRoom']:
                        roomList.remove(item)
                        check = 1
                
                if check:
                    msg += "DELETEROOM"
                    

                with open("room.json","w") as f:
                    json.dump(roomList, f, indent = 4)

                if len(msg) == 0:
                    msg += "Error"

                
            if dataR[0] == "ADDPRODUCTROOM":
                productRoom = []
                msg = ""
                with open("productRoom.json","r") as f:
                    productRoom = json.load(f)

                for item in dataR[3:]:
                    product = item.split(",")
                    print(product)
                    newProduct = {
                        "idUser": dataR[1],
                        "idRoom": dataR[2],
                        "idProduct": f"{dataR[2]}-{productIndex}",
                        "nameProduct": product[0],
                        "describeProduct": product[1],
                        "startPrice": product[2],
                        "timeAuction": product[3]
                    }
                    productRoom.append(newProduct)

                with open("productRoom.json","w") as f:
                    json.dump(productRoom, f, indent = 4)

                msg += "ADDPRODUCTROOM"





            if dataR[0] == "VIEWPRODUCTROOM":
                productRoom = []
                msg = ""
                with open("productRoom.json","r") as f:
                    productRoom = json.load(f)
                newList = [item for item in productRoom if dataR[1] == item['idUser'] and dataR[2] == item['idRoom']]
                
                
                if len(newList) > 0:
                    msg += f"VIEWPRODUCTROOM {dataR[1]} {dataR[2]}"
                    for item in newList:
                        msg += f" {item['idProduct']},{item['nameProduct']},{item['describeProduct']},{item['startPrice']},{item['timeAuction']}"
                else:
                    msg += f"VIEWPRODUCTROOM {dataR[1]}"
                if len(msg) == 0:
                    msg += "Error"


            if dataR[0] == "REMOVEPRODUCTROOM":
                productRoom = []
                listDelete = []
                msg = ""
                with open("productRoom.json","r") as f:
                    productRoom = json.load(f)
                data = dataR[3:]
                for item in productRoom:
                    if item['idUser'] == dataR[1] and item['idRoom'] == dataR[2] and item['idProduct'] in data:
                        listDelete.append(item)
                        productRoom.remove(item)

                with open("productRoom.json","w") as f:
                    json.dump(productRoom, f, indent = 4)

                if len(listDelete) > 0:
                    msg += "REMOVEPRODUCTROOM"
                else:
                    msg += "Error"

            if dataR[0] == "LISTMYROOM":
                roomList = []
                msg = ""
                with open("room.json","r") as f:
                    roomList = json.load(f)
                newList = [item for item in roomList if item.get('idUser') == dataR[1]]
                if len(newList) > 0:
                    msg += f"LISTMYROOM {dataR[1]}"
                    for item in newList:

                        msg += f" {item['idRoom']},{item['nameRoom']}"
                else:
                    msg += f"LISTMYROOM {dataR[1]}"
                if len(msg) == 0:
                    msg += "Error"

                
            if dataR[0] == "LISTROOM":
                roomList = []
                msg = ""
                with open("room.json","r") as f:
                    roomList = json.load(f)
                newList = [item for item in roomList if item.get('idUser') != dataR[1]]
                if len(newList) > 0:
                    msg += f"LISTROOM {dataR[1]}"
                    for item in newList:

                        msg += f" {item['idRoom']},{item['nameRoom']}"
                else:
                    msg += f"LISTROOM {dataR[1]}"
                if len(msg) == 0:
                    msg += "Error"
   


            if dataR[0] == "PRODUCTAUCTIONED":
                msg += "PRODUCTAUCTIONED iduser room-0-nam-0,viet,room-0-nam,nam room-0-nam-1,xetang,room-0-nam,nameRoom2"
            if dataR[0] == "PRODUCTAUCTING":
                msg += "PRODUCTAUCTING iduser idProduct3,nameProduct3,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "PRODUCTAUCTION":
                msg += "PRODUCTAUCTION iduser idProduct4,nameProduct4,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "SEARCHPRODUCTINFOR":
                msg += "SEARCHPRODUCTINFOR iduser idProduct1,nameProduct1,idRoom1,nameRoom1 idProduct2,nameProduct2,idRoom2,nameRoom2"
            if dataR[0] == "SEARCHPRODUCTTIME":
                msg += "SEARCHPRODUCTTIME iduser idProduct3,nameProduct3,idRoom3,nameRoom3 idProduct2,nameProduct2,idRoom2,nameRoom2"


            if dataR[0] == "VIEWROOM":
                nowPrice = 12
                msg += f"VIEWROOM user-1-viet12 room-0-nam RoomViet room-0-nam-1 xedap {nowPrice} 100.0 5"

            if dataR[0] == "BUYNOW":
                msg += "BUYNOW"

            if dataR[0] == "BIDPRICE":
                nowPrice = 12
                time = time - 1
                newPrice = float(dataR[3])
                price = nowPrice
                if newPrice - nowPrice > 10:
                    price = newPrice

                if price > nowPrice:
                    msg += f"BIDPRICE user-1-viet12 room-0-nam room-0-nam-1 {newPrice} {time}"
                else:
                    msg += "Error"


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