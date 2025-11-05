# Telegram Bot Factory

A powerful Telegram bot factory system that allows you to create and manage multiple bot instances from a single master bot.

---

## Overview

This project consists of two main components:
- **Master Bot (Factory)**: Takes bot tokens from users and creates bot instances
- **Template Bot**: The bot template that gets copied for each new instance

Each bot instance runs independently using screen sessions on your server.

---

## License & Copyright

```
Copyright © 2025 Ahmed Ayyad (ahmedyad200). All rights reserved.
Licensed under Custom Proprietary License
```

### Important Legal Terms:

**You MAY:**
- Use this software commercially
- Modify the code for your needs
- Deploy on multiple servers

**You MAY NOT:**
- Resell or redistribute this software
- Remove copyright notices from the code
- Share the source code publicly
- Transfer your license to others

**REQUIRED:**
- Keep all copyright notices intact in the source code
- This software is for your use only

**For full license terms, see the [LICENSE](LICENSE) file.**

---

## Requirements

- **Python**: 3.10 or higher
- **Redis**: For data storage
- **Screen**: For managing bot instances
- **Operating System**: Linux (recommended)

---

## Installation

### 1. Clone the Project

```bash
git clone https://github.com/ahmedayyad-dev/EHkBot .
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Subscribe to Required APIs

**IMPORTANT**: This bot requires a specific API from RapidAPI to function.

**Required API:**
- [YouTube to Telegram Uploader API](https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api)

**Steps:**
1. Visit the API page: https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api
2. Click "Subscribe to Test" and choose a pricing plan
3. After subscribing, go to [RapidAPI Dashboard](https://rapidapi.com/developer/dashboard)
4. Copy your RapidAPI key (you'll need it in the next step)

**WARNING: Without subscribing to this API and getting a valid key, the bot will NOT work.**

### 4. Configure Your Bot

Create a file named `info.py` in the project root with your credentials:

```python
# info.py
FBotToken = 'YOUR_BOT_TOKEN_HERE'
owner_id = YOUR_TELEGRAM_ID_HERE
rapidapi_key = 'YOUR_RAPIDAPI_KEY_HERE'
LICENSE_KEY = 'YOUR_LICENSE_KEY_HERE'
channel = 'YOUR_TELEGRAM_CHANNEL_HERE'
api_id = YOUR_APP_ID
api_hash = 'YOUR_API_HASH'
```

**Example:**
```python
FBotToken = '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'
owner_id = 944353237
rapidapi_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8'
LICENSE_KEY = 'BOTFACTORY-A1B2C3D4-E5F67893-EFYA903B'
channel = 'YYYBR'
api_id = 7720093
api_hash = '51560d96d683932d1e68851e7f0fdea2'
```

---

## Usage

### Starting the Master Bot

```bash
screen -S Master python main.py
```

The bot will:
- Verify your license automatically (embedded in the code)
- Connect to Telegram
- Wait for users to send bot tokens
- Create new bot instances in separate screen sessions

### Managing Bot Instances

List all running screen sessions:
```bash
screen -ls
```

Attach to a specific bot instance:
```bash
screen -r [session_name]
```

Detach from screen: Press `Ctrl + A`, then `D`

---

## Important Notes

1. **RapidAPI Subscription**: You MUST subscribe to the [YouTube to Telegram Uploader API](https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api). The bot will not function without a valid subscription and API key.

2. **License Verification**: This software includes built-in license verification. Do not attempt to modify or remove it.

3. **Copyright Notices**: All source code files contain copyright notices. These MUST remain intact as per the license agreement.

4. **Support**: This is a commercial product. Support is provided to legitimate license holders only.

5. **Server Requirements**: Ensure your server has sufficient resources to run multiple bot instances.

6. **Security**: Keep your `info.py` file secure and never share it publicly. It contains sensitive credentials.

---

## Contact & Support

- **Author**: Ahmed Ayyad (@ahmedyad200)
- **Email**: ahmedyad200@gmail.com
- **GitHub**: [@ahmedayyad-dev](https://github.com/ahmedayyad-dev)
- **Telegram**: [@Ayyad](https://t.me/Ayyad)

---

## Security Notice

This software is protected by:
- License verification system
- Code obfuscation
- Copyright protection

Any attempt to bypass these protections violates the license agreement and may result in:
- License termination
- Legal action
- Loss of support

---

## Version Information

- **Python Version**: 3.10+
- **License Type**: Custom Proprietary License
- **Copyright Year**: 2025

---

**© 2025 Ahmed Ayyad (ahmedyad200). All rights reserved.**

*This software is provided under a proprietary license. Unauthorized distribution, modification of copyright notices, or resale is strictly prohibited.*