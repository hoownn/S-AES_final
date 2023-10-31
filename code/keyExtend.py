def str_to_int(a:str)->int:
    '''
    将str类型的二进制表示转换为可以异或的整数
    '''
    i = len(a)-1
    n = 0
    s = 0
    while i >= 0:
        s += int(a[i])*(2**n)
        i -= 1
        n += 1
    return s


def subNib(a)->str:
    '''
    替换盒
    将八位的a分为两两一组，共4组
    把两个拼起来，得到一个数字
    '''
    s_box = [[9,4,10,11],
            [13,1,8,5],
            [6,2,0,3],
            [12,14,15,7]]

    # 将八位的a分为两两一组，共4组
    # 要把两个拼起来，得到一个数字
    n = get_num(a)
    return bin(s_box[n[0]][n[1]])[2:].zfill(4)+bin(s_box[n[2]][n[3]])[2:].zfill(4)

def get_num(a):
    '''
    把八位异或结果a的01,23,45,67拼起来
    '''

    a = list(a)
    for i in range(len(a)):
        a[i] = int(a[i])
    r = a[0]*2 + a[1], a[2]*2 + a[3], a[4]*2 + a[5], a[6]*2 + a[7]
    return r

def rotNib(w:str)->str:
    '''
    交换前四位和后四位
    '''
    temp = w[:4]
    return w[4:] + temp  

def key_extend(k0:str):
    # key0 = '0010110101010101'
    key0 = k0
    w0 = key0[:8]
    w1 = key0[8:]
    RCON = ['10000000','00110000']
    # w1_rotNib = rotNib(w1)
    # print(w1_rotNib)
    # print(S_boxs(w1_rotNib)) #对咯！
    w2 = str_to_int(w0)^str_to_int(RCON[0])^str_to_int(subNib(rotNib(w1)))#返回int
    # print(bin(w2)[2:].zfill(8))
    w3 = w2^str_to_int(w1) #返回int
    w4 = w2^str_to_int(RCON[1])^str_to_int(subNib(rotNib(bin(w3)[2:].zfill(8))))
    w5 = w4^w3
    return w0,w1,bin(w2)[2:].zfill(8),bin(w3)[2:].zfill(8),bin(w4)[2:].zfill(8),bin(w5)[2:].zfill(8)

if __name__ == '__main__':
    key0 = '0010110101010101'
    print(key_extend(key0))

