#!/usr/bin/env python3
"""
GitHub 2FA TOTP 验证码生成器

用法:
  python totp.py add <名称> <密钥>    # 添加一个账号
  python totp.py list                 # 列出所有账号
  python totp.py <名称>               # 生成指定账号的验证码
  python totp.py                      # 生成所有账号的验证码
  python totp.py remove <名称>        # 删除一个账号
  python totp.py qr <名称>            # 显示密钥的二维码(需要 qrcode 库)
"""

import base64
import hashlib
import hmac
import json
import struct
import sys
import time
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "secrets.json"


def generate_totp(secret: str, period: int = 30, digits: int = 6) -> str:
    """根据密钥生成 TOTP 验证码"""
    # 解码 Base32 密钥
    key = base64.b32decode(secret.upper().strip().replace(" ", ""), casefold=True)

    # 计算时间步
    counter = int(time.time()) // period

    # HMAC-SHA1
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # 动态截断
    offset = hmac_hash[-1] & 0x0F
    code = struct.unpack(">I", hmac_hash[offset : offset + 4])[0]
    code &= 0x7FFFFFFF
    code %= 10**digits

    return str(code).zfill(digits)


def get_remaining_seconds(period: int = 30) -> int:
    """获取当前验证码剩余有效秒数"""
    return period - (int(time.time()) % period)


def load_secrets() -> dict:
    """加载保存的密钥"""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}


def save_secrets(secrets: dict):
    """保存密钥到文件"""
    CONFIG_FILE.write_text(json.dumps(secrets, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_add(name: str, secret: str):
    secrets = load_secrets()
    secrets[name] = secret.upper().strip().replace(" ", "")
    save_secrets(secrets)
    print(f"已添加账号: {name}")


def cmd_remove(name: str):
    secrets = load_secrets()
    if name not in secrets:
        print(f"账号不存在: {name}")
        return
    del secrets[name]
    save_secrets(secrets)
    print(f"已删除账号: {name}")


def cmd_list():
    secrets = load_secrets()
    if not secrets:
        print("还没有添加任何账号。")
        print("使用 python totp.py add <名称> <密钥> 来添加。")
        return
    print("已保存的账号:")
    for name in secrets:
        print(f"  - {name}")


def show_code(name: str, secret: str):
    code = generate_totp(secret)
    remaining = get_remaining_seconds()
    bar_len = 20
    filled = int(bar_len * remaining / 30)
    bar = "#" * filled + "-" * (bar_len - filled)
    print(f"  {name}: {code}  [{bar}] {remaining}s")


def cmd_generate(name: str | None = None):
    secrets = load_secrets()
    if not secrets:
        print("还没有添加任何账号。")
        print("使用 python totp.py add <名称> <密钥> 来添加。")
        return

    if name:
        if name not in secrets:
            print(f"账号不存在: {name}")
            return
        show_code(name, secrets[name])
    else:
        print()
        for n, s in secrets.items():
            show_code(n, s)
        print()


def cmd_qr(name: str):
    """在终端显示密钥对应的二维码"""
    secrets = load_secrets()
    if name not in secrets:
        print(f"账号不存在: {name}")
        return

    try:
        import qrcode
    except ImportError:
        print("需要安装 qrcode 库: pip install qrcode")
        return

    secret = secrets[name]
    uri = f"otpauth://totp/GitHub:{name}?secret={secret}&issuer=GitHub"
    qr = qrcode.QRCode(border=1)
    qr.add_data(uri)
    qr.make(fit=True)
    qr.print_ascii(invert=True)


def main():
    args = sys.argv[1:]

    if not args:
        cmd_generate()
        return

    match args[0]:
        case "add":
            if len(args) < 3:
                print("用法: python totp.py add <名称> <密钥>")
                return
            cmd_add(args[1], args[2])
        case "remove":
            if len(args) < 2:
                print("用法: python totp.py remove <名称>")
                return
            cmd_remove(args[1])
        case "list":
            cmd_list()
        case "qr":
            if len(args) < 2:
                print("用法: python totp.py qr <名称>")
                return
            cmd_qr(args[1])
        case _:
            cmd_generate(args[0])


if __name__ == "__main__":
    main()
