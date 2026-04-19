[English](README.md)

# 2FA 验证器

基于 TOTP（RFC 6238）的双因素认证验证码生成器，支持网页版和命令行版。

## 功能

- **网页版** — 圆环倒计时、点击一键复制、多账号管理、支持中英文切换
- **命令行版** — 零依赖、纯 Python 标准库实现
- **通用兼容** — 支持 GitHub、Google、Microsoft、Steam 等所有使用 TOTP 的服务
- **数据本地存储** — 密钥保存在浏览器 localStorage / 本地文件，不上传任何地方

## 快速开始

### 网页版（推荐）

双击 `验证码.bat` 即可在浏览器中打开。

1. 点击 **添加**，输入名称和密钥
2. 点击验证码即可复制到剪贴板
3. 圆环倒计时显示剩余有效时间（绿色 → 黄色 → 红色）
4. 点击标题旁的 **EN/中文** 按钮可切换语言

### 命令行版

```bash
# 添加账号
python totp.py add github YOUR_SECRET_KEY

# 生成验证码
python totp.py github

# 列出所有账号
python totp.py list

# 删除账号
python totp.py remove github
```

## 如何获取密钥

以 GitHub 为例：

1. Settings → Password and authentication → Two-factor authentication
2. 点击 Authenticator app 的 **Edit**
3. 点击 **setup key** 链接，即可看到你的密钥（Base32 格式）
4. 将密钥添加到本工具中

## 原理

```
密钥 (Secret Key) + 当前时间 → HMAC-SHA1 → 动态截断 → 6位验证码
```

- 算法公开（RFC 6238），安全性依赖密钥保密
- 验证码每 30 秒自动更新，防止被截获重用
- 密钥只存储在本地设备上，不会上传到任何服务器

## 技术栈

- 前端：原生 HTML/CSS/JavaScript + Web Crypto API
- 后端：Python 标准库（hashlib, hmac, base64）
- 无第三方依赖

## License

MIT
