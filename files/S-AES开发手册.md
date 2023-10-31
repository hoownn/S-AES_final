# S-AES开发手册

本项目主要分为S-AES算法设计和图形用户界面（GUI）设计两大部分

## 一、S-AES算法设计

### 1.S-AES算法原理讲解

S-AES是AES的简化版本，其只使用了16位的明文和16位的密钥进行加密。

![](./images/t1.png)

具体算法详解可查看附件S-AES.pdf

### 2.文件详情

![](./images/p1.2.2.png)

###### main.py：S-AES加解密主函数

​     encrypt()：基础的单重加密函数

​    decrypt()：基础的单重解密函数

​    encrypt_0()：单重加密函数，可识别输入的明文为字符串或二进制并调用encrypt()进行加密，并返回对应格式                     

​                            的加密结果。

​    decrypt_0()：单重解密函数，可识别输入的密文为字符串或二进制并调用decrypt()函数进行加密，并返回对应                    

​                            格式的解密结果。

​    bi_encrypt()：双重加密函数，同样可以识别输入的明文为字符串或二进制数据。

​    bi_decrypt()：双重解密函数，同样可以识别输入的密文为字符串或二进制数据。

​    tri_encrypt()：三重加密函数，按照32bits密钥Key(K1+K2)的模式进行三重加密，同样可以识别输入的明文为字

​                             符串或二进制数据。

​    tri_decrypt()：三重解密函数，按照32bits密钥Key(K1+K2)的模式进行三重解密，同样可以识别输入的明文为字

​                             符串或二进制数据。

​    cbc_encrypt()：密码分组链(CBC)模式加密函数，可以对较长的明文消息进行加密，初始向量(IV)为人为输入。

​    cbc_decrypt()：密码分组链(CBC)模式解密函数，可以对较长的明文消息进行解密，初始向量(IV)为人为输入。

###### halfByteSub.py：半字节代替变换

​    halfByteSub()：半字节代替函数。

​    C_halfByteSub：逆半字节代替函数。

​    get_num()：半字节代替S盒对应的辅助函数。

###### keyAddition.py：轮密钥加

​    key_addition()：轮密钥加函数。

###### keyExtend.py：扩展密钥

​    key_extend()：密钥扩展函数。

###### rowcolumnChange.py：行位移和列混淆，同时包含CBC模式中的异或操作

​    gf_multiply()：GF(2^4)。

​    rowChange()：行位移，逆行位移与行位移实现一样。

​    colChange()：列混淆函数。

​    c_colChange()：逆列混淆函数。

​    xor_blocks()：异或操作函数。

###### MITAttack.py：中间相遇攻击关卡测试

## 二、图形用户界面设计

### 1.整体效果展示

图形用户界面（GUI）使用PyQT5实现，主要包含三个数据输入框（明密文的输入框、原始密钥输入框、初始向量输入框），四个模式选择按钮（普通模式、双重加密模式、三重加密模式、CBC模式），两个加解密按钮（加密按钮、解密按钮），以及一个加解密结果展示区组成。

![](./images/p1.2.3.png)

当加解密后，下方信息框会返回加解密的明密文、密钥、初始向量及加解密结果。

![](./images/p2.3.3.png)



### 2.文件详情

![](./images/p1.2.2.png)

###### SAES.ui文件：QTDesigner绘制的GUI文件

###### ui.py文件：将S-AES算法的各种加解密函数与GUI相连接

引入SAES.ui文件，将四个单选按钮分别与之相对应的加解密函数链接，实现加解密模式的选择。

```
    def init_ui(self):
        self.ui = uic.loadUi("./SAES.ui")
        binEdit = self.ui.TextlineEdit  # 明密文输入框
        keyEdit = self.ui.KeylineEdit  # 密钥输入框
        ivEdit = self.ui.IVlineEdit    # 初始向量输入框
        encryptBtn = self.ui.EncryptButton  # 加密按钮
        decrypthBtn = self.ui.DecrypthButton  # 解密按钮

        radioButton = self.ui.radioButton  # 普通模式
        radioButton_2 = self.ui.radioButton_2  # 双重加密
        radioButton_3 = self.ui.radioButton_3  # 三重加密
        radioButton_4 = self.ui.radioButton_4  # CBC加密

        MessageBsr = self.ui.MessageBrowser  # 信息显示区域
# 连接单选按钮的 toggled 信号到不同的加密和解密函数
        # 普通模式
        radioButton.toggled.connect(lambda checked: encryptBtn.clicked.connect(
            lambda: MessageBsr.setText(encrypt_0(binEdit.text(), keyEdit.text()))) if checked else None)
        radioButton.toggled.connect(lambda checked: decrypthBtn.clicked.connect(
            lambda: MessageBsr.setText(decrypt_0(binEdit.text(), keyEdit.text()))) if checked else None)
        # 双重加密模式
        radioButton_2.toggled.connect(lambda checked: encryptBtn.clicked.connect(
            lambda: MessageBsr.setText(bi_encrypt(binEdit.text(), keyEdit.text()))) if checked else None)
        radioButton_2.toggled.connect(lambda checked: decrypthBtn.clicked.connect(
            lambda: MessageBsr.setText(bi_decrypt(binEdit.text(), keyEdit.text()))) if checked else None)
        # 三重加密模式
        radioButton_3.toggled.connect(lambda checked: encryptBtn.clicked.connect(
            lambda: MessageBsr.setText(tri_encrypt(binEdit.text(), keyEdit.text()))) if checked else None)
        radioButton_3.toggled.connect(lambda checked: decrypthBtn.clicked.connect(
            lambda: MessageBsr.setText(tri_decrypt(binEdit.text(), keyEdit.text()))) if checked else None)
        # CBC加密模式
        radioButton_4.toggled.connect(lambda checked: encryptBtn.clicked.connect(
            lambda: MessageBsr.setText(cbc_encrypt(binEdit.text(), keyEdit.text(), ivEdit.text()))) if checked else None)
        radioButton_4.toggled.connect(lambda checked: decrypthBtn.clicked.connect(
            lambda: MessageBsr.setText(cbc_decrypt(binEdit.text(), keyEdit.text(), ivEdit.text()))) if checked else None)
```

