from socket import *
import getpass
from time import sleep

ADDR = ("127.0.0.1", 8888)

page1 = """
=====================================

            Dictionary

            1. sign in
            2. sign up
            3. exit

=====================================

"""

page2 = """
=====================================

            1. check a word
            2. sign out
            3. exit dictionary

=====================================

"""





def signin():
    while True:
        print(page2)
        opt2 = input("Please enter your order:")
        if opt2 == "check a word":
            print("dictionary")
        elif opt2 == "sign out":
            return 2
        elif opt2 == "exit dictionary":
            return 3
        else:
            print("Please enter a right order.")
            continue

def signin_test():
    account = input("Username:")
    pwd = getpass.getpass("Password:")
    user = (account, pwd)
    s.send(str(user).encode())# 需要嵌入验证账户信息
    key = s.recv(32).decode()
    if key == "pass":
        print("pass")
        return 1
    else:
        print("Account does not exist...")
        return 

def signup():
    while True:
        account = input("Username:").encode()
        s.send(account)
        sleep(0.1)
        key = s.recv(128).decode()
        if key == "block": # 用户名重复，此处就不设置退出，也就是说不设置成功不许正常退出
            print("Existing username...")
            continue
        pwd = getpass.getpass("Password:")
        pwd_veri = getpass.getpass("Please renter your password:")
        if pwd == pwd_veri:
            s.send(pwd.encode())
            sleep(0.1)
            print("Successful login!")
            break 
    return


s = socket()
s.connect(ADDR)
data = s.recv(4096).decode()
if data == "connecting":
    while True:
        print(page1)
        opt = input("Please enter your order:").strip()
        if opt == "sign in":#sign in的操作一共有四种可能，登录成功，登录失败，登录成功后退出程序，异常
            s.send(b'1')
            sleep(0.1)            
            if not signin_test():#如果登录失败，则重新回到主页
                continue
            ans = signin()#如果登录成功，则进入sign in函数
            if ans == 3:#如果登录成功后退出程序，则直接退出while关闭套接字，这里不在signin函数里直接关闭套接字是为了避免关闭后再次运行到后面的s.close()造成bug
                s.send(b'3')
                break
            else:#如果出现异常，则重新输入
                continue
        elif opt == "sign up":#sign up的操作一共有三种可能，注册成功-回到主页，注册失败-回到主页，异常-回到主页
            s.send(b'2')
            sleep(0.1)
            signup()
            continue
        elif opt == "exit":#客户端请求退出
            s.send(b'3')
            break
        else:#客户输入命令出错
            print("Please enter a right order.")
            continue
s.close()
