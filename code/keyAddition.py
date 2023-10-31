def key_addition(state, round_key):
    """
    执行密钥加操作，使用给定的轮密钥对状态数组进行异或操作。
    :param state: 16位的状态数组。
    :param round_key: 16位的轮密钥。
    :return: 经过密钥加操作后的状态数组。
    """
    # 确保数据和密钥都是16位
    assert len(state) == 16
    assert len(round_key) == 16

    # 进行异或操作
    list = ''
    for i in range(16):
        # Python中的^符号表示异或操作
        list += str(int(state[i]) ^ int(round_key[i]))

    return list


if __name__ == '__main__':
    bin_data = input("请输入明文：")
    key_0 = input("请输入密钥：")

    print("输入明文为：", bin_data)
    print("输入密钥为：", key_0)

    print("轮密钥加结果：", key_addition(bin_data, key_0))
