# Monad Token Distributor / Monad代币批量转账器

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![Web3.py](https://img.shields.io/badge/Web3.py-5.0%2B-orange)

A PyQt5-based desktop application for distributing native tokens on the Monad testnet. This tool allows you to send MON tokens to multiple addresses efficiently.

一个基于 PyQt5 的桌面应用程序，用于在 Monad 测试网上分发原生代币。该工具可以高效地向多个地址发送 MON 代币。

---

## Features / 功能

- **Easy-to-use GUI**: Built with PyQt5 for a seamless user experience.  
  **易于使用的 GUI**：使用 PyQt5 构建，提供流畅的用户体验。
- **Batch Transfers**: Send tokens to multiple addresses in one go.  
  **批量转账**：一次性向多个地址发送代币。
- **Dynamic Gas Pricing**: Automatically fetches the current gas price from the network.  
  **动态 Gas 价格**：自动从网络获取当前的 Gas 价格。
- **Address Validation**: Ensures all recipient addresses are valid before sending.  
  **地址验证**：在发送前确保所有接收地址有效。
- **Transaction Logging**: Logs all transaction details for easy tracking.  
  **交易日志**：记录所有交易详情，方便追踪。

---

## Requirements / 环境要求

- Python 3.8+
- PyQt5
- Web3.py

---

## Configuration / 配置
“giver.txt”：
This file should contain the private key of the wallet used for distributing tokens.
该文件应包含用于分发代币的钱包私钥。

## Usage / 使用说明
Run the application / 运行程序：
--python main.py


Enter recipient addresses / 输入接收者地址：

In the "Recipient Addresses" field, enter one address per line.
在“接收者地址”字段中，每行输入一个地址。

Set the amount / 设置金额：

Enter the amount of MON tokens to send to each address.
输入要发送给每个地址的 MON 代币数量。

Start distribution / 开始分发：

Click the "Start Transfer" button to begin sending tokens.
点击“开始转账”按钮，开始发送代币。

![image](https://github.com/user-attachments/assets/9244f86e-3c3d-4d48-aa17-2635889f030a)


## Author：Liam

## Twitter: @liamberich

## Support / 支持
If you find this project helpful, consider supporting it by:
如果你觉得本项目有帮助，可以通过以下方式支持：

⭐ Starring this repository.
⭐ 给本仓库点个 Star。

🐛 Reporting issues.
🐛 报告问题。

💡 Suggesting new features.
💡 提出新功能建议。
