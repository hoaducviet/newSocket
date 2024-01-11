import socket
import json
import signup
import signin
import logProductBuy
import logAuctionJoin
import createRoomAuction
import removeRoomAuction
import addProductRoomAuction
import removeProductRoomAuction
import listProductRoomAuction
import listRoom
import productAuction
import searchProduct
import editPassword
import viewRoom


HOST = '127.0.0.1'  
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to port ' + str(server_address))
s.connect(server_address)


userSignUp = signup.SignUp(s)
userSignIn = signin.SignIn(s)
userLogProduct = logProductBuy.LogUser(s)
userLogAuction = logAuctionJoin.LogAuction(s)
createNewRoom = createRoomAuction.CreateRoomAuction(s)
newPassword = editPassword.EditPassword(s,1)


def managerRoomScreen(idRoom, nameRoom):
    while True: 
        print("\nQuản lý phòng {}\n1.Danh sách vật phẩm\n2.Thêm vật phẩm vào danh sách\n3.Xoá vật phẩm khỏi danh sách\n4.Xem phiên đấu Giá\n5.Xoá phòng\n6.Trở lại".format(nameRoom))
        case = int(input("Lựa chọn: "))
        if case == 1:
            print("Danh sách vật phẩm")
            listProductRoomAuction.ListProductRoomAuction(s,idRoom).viewProductRoom()
        elif case == 2:
            print("Thêm vật phẩm vào danh sách")
            addProductRoomAuction.AddProductRoomAuction(s,idRoom).addProductRoomAuction()
        
        elif case == 3:
            print("Xoá vật phẩm khỏi danh sách")
            removeProductRoomAuction.RemoveProductRoomAuction(s,idRoom).removeProductRoomAuction()
        
        elif case == 4:
            print("Xem phiên đấu giá")
            viewRoom.ViewRoom(s,idRoom).viewRoom()
        elif case == 5:
            print("Xoá phòng")
            removeRoomAuction.RemoveRoomAuction(s,idRoom).removeRoom()
            break
        elif case == 6:
            break


def roomScreen():
    while True: 
        print("\nPhòng Đấu Giá\n1.Tạo phòng đấu giá\n2.Phòng đấu giá đã tạo\n3.Tham gia phòng đấu giá\n4.Trở lại")
        case = int(input("Lựa chọn: "))
        if case == 1:
            print("Tạo phòng")
            idUser, idRoom, nameRoom = createNewRoom.createRoom()
            managerRoomScreen(idRoom, nameRoom)
            
        elif case == 2:
            print("Phòng đấu giá đã tạo")
            myRoom = listRoom.ListRoom(s,1).listRoom()
            if myRoom:
                managerRoomScreen(myRoom[0],myRoom[1])

        elif case == 3:
            print("Tham gia phòng")
            room = listRoom.ListRoom(s,0).listRoom()
            viewRoom.ViewRoom(s,room[0]).viewRoom()

        elif case == 4:
            break

def listProductScreen():
    while True:
        print("\nDanh Sách Vật Phẩm\n1.Vật phẩm đã đấu giá\n2.Vật phẩm đang đấu giá\n3.Vật phẩm sắp đấu giá\n4.Tìm kiếm vật phẩm\n5.Trở lại")
        case = int(input("Lựa chọn: "))

        if case == 1:
            print("Vật phẩm đã đấu giá")
            room = productAuction.ProductAuction(s,"PRODUCTAUCTIONED").productAuction()
            viewRoom.ViewRoom(s,room[0]).viewRoom()
           
        elif case == 2:
            print("Vật phẩm đang đấu giá")
            room = productAuction.ProductAuction(s,"PRODUCTAUCTING").productAuction()
            viewRoom.ViewRoom(s,room[0]).viewRoom()

        elif case == 3:
            print("Sản phẩm sắp đấu giá")
            room = productAuction.ProductAuction(s,"PRODUCTAUCTION").productAuction()
            viewRoom.ViewRoom(s,room[0]).viewRoom()

        if case == 4:
           print("Tìm kiếm vật phẩm")
           room = searchProduct.SearchProduct(s).searchProduct()
           viewRoom.ViewRoom(s,room[0]).viewRoom()

        elif case == 5:
            break

def logUserScreen():
    while True:
        print("\nLịch Sử Người Dùng\n1.Danh sách vật phẩm đã mua\n2.Danh sách phiên đấu giá đã tham gia\n3.Trở lại")
        case = int(input("Lựa chọn: "))
        if case == 1:
            userLogProduct.logProductBuy()

        elif case == 2:
            userLogAuction.logAuctionJoin()

        elif case == 3:
            break

def mainScreen():
    while True:
        print("\n Màn Hình Chính\n1.Phòng đấu giá\n2.Danh sách vật phẩm\n3.Quản lý lịch sử người dùng\n4.Đổi mật khẩu\n5.Đăng xuất")
        case = int(input("Lựa chọn: "))
        if case == 1:
            roomScreen()
        elif case == 2:
            listProductScreen()
        elif case == 3:
            logUserScreen()
        elif case == 4:
            newPassword.editPassword()
            inputScreen()
        elif case == 5:
            with open("session.json","w") as f:
                json.dump(" ", f)
            break
    

def inputScreen():
    while True:
        print("\n1.Đăng Nhập\n2.Đăng ký\n3.Thoát")
        case = int(input("Lựa chọn: "))
        if case == 1:

            #if userSignIn.signIn():
            mainScreen()

        elif case == 2:
            if userSignUp.signUp():
                mainScreen()
        elif case == 3:
            break


try:
    inputScreen()

finally:
    s.close()

