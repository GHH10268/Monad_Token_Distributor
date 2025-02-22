"""
Monad Token Distributor -Monad批量转账器v1.0
Author: Liam
Twitter：@liamberich
Email: your.email@example.com
Date: 2023-10-10
Description: A PyQt5-based application for distributing native tokens on the Monad testnet.
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QScrollArea
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer  # 确保导入 QSvgRenderer
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, Qt
from web3 import Web3

# 配置 RPC（这里使用原生测试币，不需要代币合约地址）
RPC_URL = "https://testnet-rpc.monad.xyz/"

# 连接到 Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# 读取分发者私钥（文件中保存的是私钥字符串）
def load_giver():
    try:
        with open("giver.txt", "r") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("giver.txt 文件为空")
            return content
    except FileNotFoundError:
        raise FileNotFoundError("giver.txt 文件未找到")
    except Exception as e:
        raise Exception(f"读取 giver.txt 文件时出错: {str(e)}")

class NativeTokenDistributor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Monad批量转账器v1.0  作者：Liam（推特：@liamberich）")
        self.setGeometry(100, 100, 600, 400)

        # 设置程序图标
        self.set_icon_from_url("https://cdn.prod.website-files.com/667c57e6f9254a4b6d914440/67b135627be8437b3cda15ae_Monad%20Logomark.svg")

        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background-color: #303030;
                color: #E0E0E0;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLineEdit, QTextEdit {
                background-color: #2e2e2e;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px;
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #10A37F;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0F8E6B;
            }
            QScrollArea {
                border: 1px solid #444444;
                border-radius: 4px;
                background-color: #2e2e2e;
            }
            QLabel {
                background-color: #303030;
                padding: 6px;
                border-radius: 4px;
            }
            QWidget::title {
                background-color: black;
                color: white;
            }
        """)

        # 主布局
        layout = QVBoxLayout()

        # 显示分发者地址及余额
        try:
            giver_private_key = load_giver()
            self.giver_account = w3.eth.account.from_key(giver_private_key)
            self.giver_label = QLabel(f"分发者地址: {self.giver_account.address}")
            self.balance_label = QLabel(f"余额: {self.get_balance()} MON")
        except Exception as e:
            self.giver_label = QLabel(f"❌ 错误: {str(e)}")
            self.balance_label = QLabel("余额: 0 MON")
            self.giver_account = None

        layout.addWidget(self.giver_label)
        layout.addWidget(self.balance_label)

        # 输入接收者地址
        self.receivers_input = QTextEdit(self)
        self.receivers_input.setPlaceholderText("请输入接收者地址，每行一个地址")
        layout.addWidget(QLabel("接收者地址:"))
        layout.addWidget(self.receivers_input)

        # 输入每个接收钱包转账金额
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("请输入每个钱包转账的金额（单位：MON）")
        self.amount_input.textChanged.connect(self.update_total)
        layout.addWidget(self.amount_input)

        # 显示总转账金额
        self.total_label = QLabel("总转账金额: 0 MON")
        layout.addWidget(self.total_label)

        # 转账按钮
        self.distribute_button = QPushButton("开始转账")
        self.distribute_button.clicked.connect(self.distribute_tokens)
        layout.addWidget(self.distribute_button)

        # 输出日志框
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def set_icon_from_url(self, url):
        # 创建网络访问管理器
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_icon_downloaded)

        # 发送网络请求
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)

    def on_icon_downloaded(self, reply):
        # 检查网络请求是否成功
        if reply.error() == QNetworkReply.NoError:
            # 读取 SVG 数据
            svg_data = reply.readAll()

            # 使用 QSvgRenderer 渲染 SVG
            renderer = QSvgRenderer(svg_data)
            if renderer.isValid():
                # 创建 QPixmap 并渲染 SVG
                pixmap = QPixmap(64, 64)  # 设置图标大小
                pixmap.fill(Qt.transparent)  # 设置背景为透明
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()

                # 设置程序图标
                self.setWindowIcon(QIcon(pixmap))
            else:
                print("❌ 无法加载 SVG 数据，请检查 URL 或 SVG 文件是否正确。")
        else:
            print(f"❌ 下载图标失败: {reply.errorString()}")

    def get_balance(self):
        if self.giver_account:
            balance = w3.eth.get_balance(self.giver_account.address)
            return w3.from_wei(balance, 'ether')
        return 0

    def update_total(self):
        # 从输入框中获取接收者地址
        receivers = self.receivers_input.toPlainText().strip().splitlines()
        receivers = [addr.strip() for addr in receivers if addr.strip()]

        if not receivers:
            self.total_label.setText("总转账金额: 0 MON")
            return

        amount_per_wallet = self.amount_input.text()
        if amount_per_wallet.replace('.', '', 1).isdigit():
            try:
                amount = float(amount_per_wallet)
                total = amount * len(receivers)
                self.total_label.setText(f"总转账金额: {total} MON")
            except:
                self.total_label.setText("总转账金额: 0 MON")
        else:
            self.total_label.setText("总转账金额: 0 MON")

    def distribute_tokens(self):
        if not self.giver_account:
            self.log_output.append("❌ 请检查分发者地址是否正确配置！")
            return

        # 从输入框中获取接收者地址
        receivers = self.receivers_input.toPlainText().strip().splitlines()
        receivers = [addr.strip() for addr in receivers if addr.strip()]

        if not receivers:
            self.log_output.append("❌ 请输入至少一个接收者地址！")
            return

        amount_per_wallet = self.amount_input.text()
        try:
            amount = float(amount_per_wallet)
        except:
            self.log_output.append("❌ 请输入有效的金额！")
            return

        starting_nonce = w3.eth.get_transaction_count(self.giver_account.address)
        nonce = starting_nonce

        for idx, receiver in enumerate(receivers):
            try:
                # 校验地址并转换为校验和格式
                receiver_checksum = Web3.to_checksum_address(receiver)

                # 获取当前 Gas Price
                gas_price = w3.eth.gas_price

                txn = {
                    'from': self.giver_account.address,
                    'to': receiver_checksum,
                    'value': w3.to_wei(amount, 'ether'),
                    'gas': 21000,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                }
                signed_txn = w3.eth.account.sign_transaction(txn, self.giver_account.key)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                self.log_output.append(f"✅ 成功发送 {amount} MON 给 {receiver_checksum}，交易哈希: {tx_hash.hex()}")
                nonce += 1
            except Exception as e:
                self.log_output.append(f"❌ 发送失败: {receiver}，错误: {str(e)}")

        self.log_output.append("🎉 转账完成！")
        self.balance_label.setText(f"余额: {self.get_balance()} MON")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NativeTokenDistributor()
    window.show()
    sys.exit(app.exec_())