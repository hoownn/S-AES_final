from keyExtend import key_extend
from rowcolumnChange import *
from halfByteSub import *
from keyAddition import *
import base64

def encrypt_0(plaintext, key0):
    """
    encrypt_0用于检测输入的是16位二进制数还是字符串，
    如果是字符串则进行拆分后分别加密后返回结果并整合，
    如果是16位二进制数字则直接进行加密后返回加密结果
    """
    if len(plaintext) == 0:
        return "请输入明文"
    if len(key0) != 16:
        return "输入的密钥长度错误,密钥必须是16bits"

    try:
        if not all(c in '01' for c in plaintext):
            # 输入为字符串
            results = [encrypt(format(ord(i), '016b'), key0) for i in plaintext]
            return f"输入明文为：{plaintext}\n输入密钥为：{key0}\n加密结果为：{''.join([chr(int(t, 2)) for t in results])}"
        else:
            # 输入为16位二进制数
            if len(plaintext) != 16:
                return "输入的数据长度错误,必须是16位二进制数"
            result = encrypt(plaintext, key0)
            return f"输入明文为：{plaintext}\n输入密钥为：{key0}\n加密结果为：{result}"
    except ValueError:
        return "输入数据的格式或长度有误"
def encrypt(plaintext:str,key0:str)->str:
    '''
    plaintext:16位字符串明文
    key0:16位字符串密钥
    '''
    w0, w1, w2, w3, w4, w5 = key_extend(key0)
    #round 1
    #轮密钥加
    x = key_addition(plaintext, w0+w1)
    # print(x)
    #半字节代替
    x = halfByteSub(x)
    # print(x)
    #行位移&列混淆
    x = colChange(rowChange(x))
    # print(x)
    #轮密钥加
    x = key_addition(x, w2+w3)
    # print(x)

    #round 2 
    #半字节代替
    x = halfByteSub(x)
    #行位移
    x = rowChange(x)
    # print(x)
    #轮密钥加
    x = key_addition(x, w4+w5)
    return x


def decrypt_0(ciphertext, key0):
    """
    decrypt_0用于检测输入的是16位二进制数还是字符串，
    如果是字符串则进行拆分后分别解密后返回结果并组合，
    如果是16位二进制数字则直接进行解密后返回解密结果
    """
    if len(ciphertext) == 0:
        return "请输入密文"
    if len(key0) != 16:
        return "输入的密钥长度错误,密钥必须是16bits"

    try:
        if not all(c in '01' for c in ciphertext):
            # 输入为字符串
            results = [decrypt(format(ord(i), '016b'), key0) for i in ciphertext]
            return f"输入密文为：{ciphertext}\n输入密钥为：{key0}\n解密结果为：{''.join([chr(int(t, 2)) for t in results])}"
        else:
            # 输入为16位二进制数
            if len(ciphertext) != 16:
                return "输入的数据长度错误,必须是16位二进制数"
            result = decrypt(ciphertext, key0)
            return f"输入密文为：{ciphertext}\n输入密钥为：{key0}\n解密结果为：{result}"
    except ValueError:
        return "输入数据的格式或长度有误"
def decrypt(ciphertext:str,key0:str)->str:

    '''
    plaintext:16位字符串密文
    key0:16位字符串密钥
    '''
    w0, w1, w2, w3, w4, w5 = key_extend(key0)
    # round 1
    # 轮密钥加
    y = key_addition(ciphertext, w4+w5)
    # print(y)
    # 逆行移位   恰好一样
    y = rowChange(y)
    # print(y)
    # 逆半字节代替
    y = C_halfByteSub(y)
    # print(y)
    # 轮密钥加
    y = key_addition(y, w2+w3)
    # 逆列混淆
    y = c_colChange(y)
    # 逆行移位   恰好一样
    y = rowChange(y)
    # 逆半字节代替
    y = C_halfByteSub(y)
    # 轮密钥加
    y = key_addition(y, w0+w1)
    return y


def bi_encrypt(plaintext, key00):
    '''
    双重加密;
    输入:plaintext:16bits明文;key00:32bits密钥
    '''
    if len(plaintext) == 0:
        return "请输入明文"
    if len(key00) != 32:
        return "输入的密钥长度错误,双重加密密钥必须是32bits"

    key1, key2 = key00[:16], key00[16:]

    # 判断明文是否为字符串
    if not all(c in '01' for c in plaintext):
        results = [encrypt(format(ord(i), '016b'), key1) for i in plaintext]
        results = [encrypt(midtext, key2) for midtext in results]
        results = [chr(int(t, 2)) for t in results]
        return f"输入明文为：{plaintext}\n输入密钥为：{key00}\n双重加密结果为：{''.join(results)}"
    else:
        if len(plaintext) != 16:
            return "输入的数据长度错误,必须是16位二进制数"
        midtext = encrypt(plaintext, key1)
        ciphertext = encrypt(midtext, key2)
        return f"输入明文为：{plaintext}\n输入密钥为：{key00}\n双重加密结果为：{ciphertext}"


def bi_decrypt(ciphertext, key00):
    '''
    对应双重加密的解密;
    输入:ciphertext:16bits密文;key00:32bits密钥
    '''
    if len(ciphertext) == 0:
        return "请输入密文"
    if len(key00) != 32:
        return "输入的密钥长度错误,双重解密密钥必须是32bits"

    key1, key2 = key00[:16], key00[16:]

    # 判断密文是否为字符串
    if not all(c in '01' for c in ciphertext):
        results = [decrypt(format(ord(i), '016b'), key2) for i in ciphertext]
        results = [decrypt(midtext, key1) for midtext in results]
        results = [chr(int(t, 2)) for t in results]
        return f"输入密文为：{ciphertext}\n输入密钥为：{key00}\n双重解密结果为：{''.join(results)}"
    else:
        if len(ciphertext) != 16:
            return "输入的数据长度错误,必须是16位二进制数"
        midtext = decrypt(ciphertext, key2)
        plaintext = decrypt(midtext, key1)
        return f"输入密文为：{ciphertext}\n输入密钥为：{key00}\n双重解密结果为：{plaintext}"


def tri_encrypt(plaintext, key00):
    '''
    采用方案一进行三重加密
    '''
    if len(plaintext) == 0:
        return "请输入明文"
    if len(key00) != 32:
        return "输入的密钥长度错误,三重加密密钥必须是32bits"

    key1, key2 = key00[:16], key00[16:]

    # 判断明文是否为字符串
    if not all(c in '01' for c in plaintext):
        results = [encrypt(encrypt(format(ord(i), '016b'), key1), key2) for i in plaintext]
        results = [encrypt(midtext, key1) for midtext in results]
        results = [chr(int(t, 2)) for t in results]
        return f"输入明文为：{plaintext}\n输入密钥为：{key00}\n三重加密结果为：{''.join(results)}"
    else:
        if len(plaintext) != 16:
            return "输入的数据长度错误,必须是16位二进制数"
        midtext = encrypt(encrypt(plaintext, key1), key2)
        ciphertext = encrypt(midtext, key1)
        return f"输入明文为：{plaintext}\n输入密钥为：{key00}\n三重加密结果为：{ciphertext}"


def tri_decrypt(ciphertext, key00):
    if len(ciphertext) == 0:
        return "请输入密文"
    if len(key00) != 32:
        return "输入的密钥长度错误,三重解密密钥必须是32bits"

    key1, key2 = key00[:16], key00[16:]

    if not all(c in '01' for c in ciphertext):
        results = [decrypt(decrypt(format(ord(i), '016b'), key1), key2) for i in ciphertext]
        results = [decrypt(midtext, key1) for midtext in results]
        results = [chr(int(t, 2)) for t in results]
        return f"输入密文为：{ciphertext}\n输入密钥为：{key00}\n三重解密结果为：{''.join(results)}"
    else:
        if len(ciphertext) != 16:
            return "输入的数据长度错误,必须是16位二进制数"
        midtext = decrypt(decrypt(ciphertext, key1), key2)
        plaintext = decrypt(midtext, key1)
        return f"输入密文为：{ciphertext}\n输入密钥为：{key00}\n三重解密结果为：{plaintext}"


# def cbc_encrypt(plaintext: str, key0: str, iv: str) -> str:
#     '''
#     使用密码分组链模式对较长的明文消息进行加密
#     plaintext: 明文消息，长度为16bits的倍数
#     key0: 16位字符串密钥
#     iv: 16字节的初始向量
#     '''
#     if len(plaintext) == 0:
#         return "请输入明文"
#     if len(plaintext) % 16 != 0:
#         return "明长度应为16bits的倍数"
#     if len(key0) != 16:
#         return "输入的密钥长度错误,密钥必须是16bits"
#     if len(iv) != 16:
#         return "输入的初始向量错误,初始向量必须是16bits"
#
#     ciphertext = ""
#     block_size = 16
#     plain_blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]
#
#     prev_ciphertext = iv
#     for i, plain_block in enumerate(plain_blocks):
#         # 异或
#         block = xor_blocks(plain_block, prev_ciphertext)
#
#         # 使用S-AES算法对块进行加密
#         ciphertext_block = encrypt(block, key0)
#
#         # 更新前一个密文块的结果
#         prev_ciphertext = ciphertext_block
#
#         # 将加密后的块添加到最终的密文中
#         ciphertext += ciphertext_block
#
#     return f"输入明文为：{plaintext}\n输入密钥为：{key0}\n初始向量为：{iv}\nCBC加密结果为：{ciphertext}"

def cbc_encrypt(plaintext: str, key0: str, iv: str) -> str:
    '''
    使用密码分组链模式对较长的明文消息进行加密
    plaintext: 明文消息
    key0: 16位字符串密钥
    iv: 16字节的初始向量
    '''
    if len(plaintext) == 0:
        return "请输入明文"
    if len(key0) != 16:
        return "输入的密钥长度错误,密钥必须是16bits"
    if len(iv) != 16:
        return "输入的初始向量错误,初始向量必须是16bits"

    ciphertext = ""
    prev_ciphertext = iv

    try:
        # 检验输入的是否为字符串，若为字符串则分解字符串后传入加密再将结果组合
        if not all(c in '01' for c in plaintext):
            # 将字符串转换为ASCII码的二进制表示形式
            results = []
            for i in plaintext:
                # 将字符转换为字节，然后再将字节转换为二进制字符串
                plain_block = format(ord(i), '016b')

                # 异或
                block = xor_blocks(plain_block, prev_ciphertext)

                # 使用S-AES算法对块进行加密
                ciphertext_block = encrypt(block, key0)

                # 更新前一个密文块的结果
                prev_ciphertext = ciphertext_block

                encrypted_char = chr(int(ciphertext_block, 2))
                results.append(encrypted_char)
            print(results)
            return f"输入明文为：{plaintext}\n输入密钥为：{key0}\n初始向量为：{iv}\nCBC加密结果为：" + ''.join(results)
        else:
            # if len(plaintext)%16 != 0:
            #     return "输入的数据长度错误,必须是16bits的倍数"
            # 输入二进制数据而长度不为16bits的倍数时，会对明文进行0补位，会导致解密后的数据尾部多出几个0
            if len(plaintext) % 16 != 0:
                padding = 16 - (len(plaintext) % 16)
                plaintext += '0' * padding
            block_size = 16
            plain_blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]

            prev_ciphertext = iv
            for i, plain_block in enumerate(plain_blocks):
                # 异或
                block = xor_blocks(plain_block, prev_ciphertext)

                # 使用S-AES算法对块进行加密
                ciphertext_block = encrypt(block, key0)

                # 更新前一个密文块的结果
                prev_ciphertext = ciphertext_block

                # 将加密后的块添加到最终的密文中
                ciphertext += ciphertext_block

            return f"输入明文为：{plaintext}\n输入密钥为：{key0}\n初始向量为：{iv}\nCBC加密结果为：{ciphertext}"
    except ValueError:
        return "输入数据的格式或长度有误"

def cbc_decrypt(ciphertext: str, key0: str, iv: str) -> str:
    '''
    使用密码分组链模式对密文进行解密
    ciphertext: 密文消息
    key0: 16位字符串密钥
    iv: 16字节的初始向量
    '''
    if len(ciphertext) == 0:
        return "请输入密文"
    if len(key0) != 16:
        return "输入的密钥长度错误,密钥必须是16bits"
    if len(iv) != 16:
        return "输入的初始向量错误,初始向量必须是16bits"

    plaintext = ""
    prev_ciphertext = iv
    try:
        # 检验输入的是否为字符串，若为字符串则分解字符串后传入加密再将结果组合
        if not all(c in '01' for c in ciphertext):
            # 将字符串转换为ASCII码的二进制表示形式
            results = []
            for i in ciphertext:
                # 将字符转换为字节，然后再将字节转换为二进制字符串
                cipher_block = format(ord(i), '016b')

                # 对密文块进行解密
                decrypted_block = decrypt(cipher_block, key0)

                # 异或操作
                block = xor_blocks(decrypted_block, prev_ciphertext)

                # 更新前一个密文块的结果
                prev_ciphertext = cipher_block
                encrypted_char = chr(int(block, 2))
                results.append(encrypted_char)
            print(results)
            return f"输入密文为：{ciphertext}\n输入密钥为：{key0}\n初始向量为：{iv}\nCBC解密结果为：" + ''.join(results)
        else:
            if len(ciphertext) % 16 != 0:
                padding = 16 - (len(ciphertext) % 16)
                ciphertext += '0' * padding
            block_size = 16
            cipher_blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]

            prev_ciphertext = iv
            for i, cipher_block in enumerate(cipher_blocks):
                # 对密文块进行解密
                decrypted_block = decrypt(cipher_block, key0)
                # 异或操作
                block = xor_blocks(decrypted_block, prev_ciphertext)
                # 更新前一个密文块的结果
                prev_ciphertext = cipher_block
                # 将解密后的块添加到最终的明文中
                plaintext += block
            return f"输入密文为：{ciphertext}\n输入密钥为：{key0}\n初始向量为：{iv}\nCBC解密结果为：{plaintext}"
    except ValueError:
        return "输入数据的格式或长度有误"



if __name__ == '__main__':
    plaintext = '1010101010101010'
    key0 = '1010011001101011'
    key00 = '00000000000100000000000000101010'
    key00_fake = '00000000000000010101000100000011'
    IV = '0110010010100011'
    # print(encrypt(plaintext,key0))
    # print('密文:',encrypt(plaintext,key0))
    # print('明文:',decrypt(encrypt(plaintext,key0),key0))#预期输出：plaintext = '1010101010101010'
    # cphtx = bi_encrypt(plaintext,key00_fake)
    # print('双重加密的明文:',plaintext)
    # print('双重加密的密文:',cphtx)
    # print('双重加密的明文:',bi_decrypt(bi_encrypt(plaintext,key00),key00))#预期输出：plaintext = '1010101010101010'
    # print('三重加密明文:', '1010101010101010')
    # print('三重加密明文:', tri_decrypt(tri_encrypt('1010101010101010', key00), key00))
    print('CBC加密:', cbc_encrypt('00000000000100000000000000101010', '1010011001101011', '0110010010100011'))
    print('CBC解密:', cbc_decrypt('10111001010100110000101110110001', '1010011001101011', '0110010010100011'))
