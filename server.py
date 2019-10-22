from socket import *
from multiprocessing import *
from time import sleep

ADDR = ("0.0.0.0", 8888)

def main():
    server = socket()
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen(5)
    while True:
        c, addr = server.accept()
        print("connected from %s" % addr[0])
        p = Process(target = distributor, args = (c,addr))
        p.daemon = True
        p.start()#存在僵尸进程问题，如何解决

def distributor(c, addr):
    c.send(b"connecting")
    while True:
        data = c.recv(4096).decode() #data 空表示退出， 1表示登录， 2表示注册，
        if not data:
            print("Disconnected with %s" % addr[0])
            break
        #评价是否pass
        if data == "1":#用户发起登录请求
            print("sign in request")
            key = signin(c, addr)
            if key == 0:#返回0表示
                print("Disconnected with %s" % addr[0])
                break
            else:
                continue
            
        elif data == "2":
            print("sign up request")
            key = signup(c, addr)
            if key == 0:
                print("Disconnected with %s" % addr[0])
                break
            else:
                continue
        elif data == "3":
            print("Disconnected with %s" % addr[0])
            break
        elif data == "4":
            print("dictionary request")
            key = dic(c, addr)
            if key == 0:
                print("Disconnected with %s" % addr[0])
                break
            else:
                continue
    c.close()

def dic(c, addr):
    word = c.recv(4096).decode()
    if not word:
        return 0
    fr = open("dict.txt", "r+")
    item = fr.readlines()
    for 
        
def signin(c, addr):
    user = c.recv(4096).decode()
    if not user:
        return 0
    elif user == "('1111', '2222')":#这里加入搜索账户信息是否正确，正确返回pass，错误返回block
        c.send(b"pass")
        print(addr, "pass")
        return
    else:
        c.send(b"block")
        print(addr, "block")
        return    

def signup(c, addr):
    while True:
        account = c.recv(4096).decode()
        if not account:
            return 0
        elif account == "1111":
            c.send(b"block")
            sleep(0.1)
            print(addr,"invalid name")
            continue
        else:
            c.send(b"pass")
            sleep(0.1)
            print(addr,"pass")
            pwd = c.recv(1024).decode()
            new_user = (account, pwd)
            print(new_user)#此句最后需删除
            #此处处理注册信息

if __name__ == "__main__":
    main()