import os
import sys
import threading
import time
from main import decrypt, encrypt
                            #线程锁有点东西哦，，有空学一下
#参数
key_size = 16
num_thread = 8
##改成32位的密码直接，然后更合理的分配


num_key = 2**key_size
interval = num_key/num_thread

def trykey(key_init = 0,name = ''):
    try_key = key_init
    sc = 0 #这个是看这个结果是不是对所有明密文对都成立，统计成立的数量
    for j in range(int(interval)):

        k1 = bin(int(try_key+j))[2:].zfill(key_size)
        
        for k2 in range(2**key_size):
            k2 = bin(k2)[2:].zfill(key_size)
            # print('线程',name,'正在尝试密钥:k1=',k1,'k2=',k2,)
            # print()
            for i  in range(len(plain_text)) :
                if encrypt(plain_text[i],str(k1)) ==  decrypt(cipher_text[i],str(k2)):
                    sc += 1
                else :
                    break
            if sc == len(plain_text):
                print('\n密码已找到,结果为:',k1+k2)
                print('本次破解用时',time.time()-str_ti)
                sys.exit()
                # os._exit()


def t1():
    trykey(key_init = 0,name='1')
    sys.exit()
def t2():
    trykey(key_init = interval*1,name='2')
    sys.exit()
def t3():
    trykey(key_init = interval*2,name='3')
    sys.exit()
def t4():
    trykey(key_init = interval*3,name='4')
    sys.exit()
def t5():
    trykey(key_init = interval*4,name='5')
    sys.exit()
def t6():
    trykey(key_init = interval*5,name='6')
    sys.exit()
def t7():
    trykey(key_init = interval*6,name='7')
    sys.exit()
def t8():
    trykey(key_init = interval*7,name='8')
    sys.exit()
    

if __name__ == '__main__':
    #双重加密的明文: 1010101010101010
    # 双重加密的密文: 0001000010000010
    plain_text = ['1010101010101010']
    cipher_text = ['0001000010000010']
    # plain_text =['10000000']
    # cipher_text =['00000010']
    # 创建新线程
    th1 = threading.Thread(target=t1,name='t1')
    th2 = threading.Thread(target=t2,name='t2')
    th3 = threading.Thread(target=t3,name='t3')
    th4 = threading.Thread(target=t4,name='t4')
    th5 = threading.Thread(target=t5,name='t5')
    th6 = threading.Thread(target=t6,name='t6')
    th7 = threading.Thread(target=t7,name='t7')
    th8 = threading.Thread(target=t8,name='t8')
    print('开始')
    str_ti = time.time()
    th1.start()
    # print()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()
    th7.start()
    th8.start()