[中文](README.zh-CN.md)

# 2FA Authenticator

A TOTP (RFC 6238) based two-factor authentication code generator with both web and command-line interfaces.

## Features

- **Web UI** — Ring countdown timer, one-click copy, multi-account management, language toggle (EN/中文)
- **CLI** — Zero dependencies, pure Python standard library
- **Universal Compatibility** — Works with GitHub, Google, Microsoft, Steam, and all TOTP-based services
- **Local Storage** — Keys are saved in browser localStorage / local files, never uploaded anywhere

## Quick Start

### Web UI (Recommended)

Double-click `验证码.bat` to open in your browser.

1. Click **Add**, enter a name and secret key
2. Click the code to copy it to clipboard
3. The ring countdown shows remaining validity time (green → yellow → red)
4. Click the **EN/中文** button to switch language

### CLI

```bash
# Add account
python totp.py add github YOUR_SECRET_KEY

# Generate code
python totp.py github

# List all accounts
python totp.py list

# Remove account
python totp.py remove github
```

## How to Get Your Secret Key

Using GitHub as an example:

1. Settings → Password and authentication → Two-factor authentication
2. Click **Edit** on Authenticator app
3. Click the **setup key** link to view your key (Base32 format)
4. Add the key to this tool

## How It Works

```
Secret Key + Current Time → HMAC-SHA1 → Dynamic Truncation → 6-digit Code
```

- Algorithm is public (RFC 6238), security relies on keeping the secret key private
- Codes auto-refresh every 30 seconds to prevent replay attacks
- Keys are stored locally only, never uploaded to any server

## Tech Stack

- Frontend: Vanilla HTML/CSS/JavaScript + Web Crypto API
- Backend: Python standard library (hashlib, hmac, base64)
- No third-party dependencies

## License

MIT
