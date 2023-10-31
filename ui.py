from main import *

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.setWindowTitle('S-AES算法')
    w.ui.show()

    app.exec_()