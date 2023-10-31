def halfByteSub(a: str) -> str:
    '''
    半字节代替变换
    将16位的a分为两两一组，共8组
    把两个拼起来，得到一个数字
    :param a: 16位数据。
    :return: 16位经过半字节代替变换后的数据
    '''
    # s盒
    sbox = [[9, 4, 10, 11],
            [13, 1, 8, 5],
            [6, 2, 0, 3],
            [12, 14, 15, 7]]

    n = get_num(a)
    # print(n)
    return bin(sbox[n[0]][n[1]])[2:].zfill(4) + bin(sbox[n[2]][n[3]])[2:].zfill(4)\
        + bin(sbox[n[4]][n[5]])[2:].zfill(4) + bin(sbox[n[6]][n[7]])[2:].zfill(4)

def C_halfByteSub(a: str) -> str:
    '''
    逆半字节代替变换
    将16位的a分为两两一组，共8组
    把两个拼起来，得到一个数字
    '''
    # 逆s盒
    c_sbox = [[10, 5, 9, 11],
              [1, 7, 8, 15],
              [6, 0, 2, 3],
              [12, 4, 13, 14]]

    n = get_num(a)
    # print(n)
    return bin(c_sbox[n[0]][n[1]])[2:].zfill(4) + bin(c_sbox[n[2]][n[3]])[2:].zfill(4)\
        + bin(c_sbox[n[4]][n[5]])[2:].zfill(4) + bin(c_sbox[n[6]][n[7]])[2:].zfill(4)

def get_num(a):
    """
    把16位异或结果a的01, 23, 45, 67, 89, 10 11, 12 13, 14 15拼起来
    """
    a = list(a)
    for i in range(len(a)):
        a[i] = int(a[i])
    r = a[0] * 2 + a[1], a[2] * 2 + a[3], a[4] * 2 + a[5], a[6] * 2 + a[7], a[8] * 2 + a[9], a[10] * 2 + a[11], a[
        12] * 2 + a[13], a[14] * 2 + a[15]
    return r

if __name__ == '__main__':
    # 测试
    data = '1000101000011100'

    result = halfByteSub(data)
    print("加密结果:", result)
