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

- **Operating System**: Debian 12 or Debian 13 (**REQUIRED**)
- **Python**: 3.10.12 (automatically installed by the setup script)
- **Redis**: For data storage (automatically installed)
- **Screen**: For managing bot instances (automatically installed)
- **Root Access**: Required for installation
- **Internet Connection**: Stable connection required for installation

---

## ⚠️ IMPORTANT: License Key Required

**This software requires a valid license key to function.**

### How to Get a License Key:

Before installation, you **MUST** purchase a license key from the developer:

**Contact Information:**
- **Email**: ahmedyad200@gmail.com
- **Telegram**: [@Ayyad](https://t.me/Ayyad)
- **GitHub**: [@ahmedayyad-dev](https://github.com/ahmedayyad-dev)

**Without a valid license key, the bot will NOT work.** Please contact the developer to purchase your license before proceeding with installation.

---

## Required API Subscription

**IMPORTANT**: This bot requires a specific API from RapidAPI to function.

**Required API:**
- [YouTube to Telegram Uploader API](https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api)

**Steps to Subscribe:**
1. Visit the API page: https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api
2. Click "Subscribe to Test" and choose a pricing plan
3. After subscribing, go to [RapidAPI Dashboard](https://rapidapi.com/developer/dashboard)
4. Copy your RapidAPI key (you'll need it during installation)

**WARNING: Without subscribing to this API and getting a valid key, the bot will NOT work.**

---

## Installation

### Quick Installation (Recommended)

Run this single command as root to install everything automatically:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/ahmedayyad-dev/EHkBot/refs/heads/master/setup_and_run.sh)
```

The installation script will:
1. **Ask you for the following information** (have them ready):
   - Bot Token (from @BotFather)
   - Your Telegram User ID
   - RapidAPI Key (from the subscription above)
   - **License Key** (purchased from the developer)
   - Telegram Channel username
   - API ID (from my.telegram.org)
   - API Hash (from my.telegram.org)

2. **Automatically**:
   - Clone the project repository
   - Create the configuration file
   - Install Python 3.10.12 using pyenv
   - Set up a virtual environment
   - Install all required dependencies
   - Start the bot in a screen session

### What You Need Before Installation:

1. ✅ **License Key** - Contact ahmedyad200@gmail.com or @Ayyad on Telegram
2. ✅ **RapidAPI Subscription** - Subscribe to the YouTube to Telegram Uploader API
3. ✅ **Bot Token** - Create a bot via @BotFather on Telegram
4. ✅ **Telegram API Credentials** - Get api_id and api_hash from https://my.telegram.org
5. ✅ **Your Telegram User ID** - Use @userinfobot on Telegram to get it
6. ✅ **Channel Username** - Your Telegram channel (without @)

---

## Usage

### Checking Bot Status

The bot runs in a screen session called `MainBot`. To view it:

```bash
screen -r MainBot
```

To detach from the screen session: Press `Ctrl + A`, then `D`

### Managing Bot Instances

List all running screen sessions:
```bash
screen -ls
```

Attach to a specific bot instance:
```bash
screen -r [session_name]
```

### Restarting the Bot

If you need to restart the bot:

```bash
screen -S MainBot -X quit  # Stop the current session
cd /root
source venv/bin/activate
screen -dmS MainBot python3 main.py
```

---

## Post-Installation

After successful installation:

1. The bot will be running automatically in a screen session
2. Virtual environment will activate automatically on SSH login
3. All configurations are saved in `/root/info.py`
4. Bot logs can be viewed by attaching to the screen session

---

## Important Notes

1. **Operating System Requirement**: This software is designed and tested ONLY on **Debian 12 or Debian 13**. Other Linux distributions (Ubuntu, CentOS, etc.) are NOT supported and may cause installation failures or unexpected errors.

2. **License Verification**: This software includes built-in license verification. Do not attempt to modify or remove it. Using the software without a valid license violates the terms of service.

2. **RapidAPI Subscription**: You MUST maintain an active subscription to the [YouTube to Telegram Uploader API](https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api). The bot will not function without a valid subscription and API key.

3. **Copyright Notices**: All source code files contain copyright notices. These MUST remain intact as per the license agreement.

4. **Support**: This is a commercial product. Support is provided to legitimate license holders only.

5. **Server Requirements**: Ensure your server has sufficient resources to run multiple bot instances.

6. **Security**: Keep your `/root/info.py` file secure and never share it publicly. It contains sensitive credentials.

7. **Automatic Installation**: The setup script handles everything - Python installation, dependencies, configuration, and bot startup.

---

## Troubleshooting

### Installation Issues

If the installation fails:
1. Make sure you're running as root: `sudo su`
2. Ensure you have a stable internet connection
3. Check that all required information is correct
4. Contact support if issues persist

### Bot Not Starting

If the bot doesn't start:
1. Check the screen session: `screen -r MainBot`
2. Verify your license key is valid
3. Ensure RapidAPI subscription is active
4. Check logs for error messages

### Need Help?

Contact the developer:
- **Email**: ahmedyad200@gmail.com
- **Telegram**: [@Ayyad](https://t.me/Ayyad)

---

## Contact & Support

- **Author**: Ahmed Ayyad (@ahmedyad200)
- **Email**: ahmedyad200@gmail.com
- **GitHub**: [@ahmedayyad-dev](https://github.com/ahmedayyad-dev)
- **Telegram**: [@Ayyad](https://t.me/Ayyad)

**For license purchases, technical support, or any inquiries, please contact via email or Telegram.**

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

- **Python Version**: 3.10.12
- **License Type**: Custom Proprietary License
- **Copyright Year**: 2025
- **Installation Method**: One-command automated setup

---

**© 2025 Ahmed Ayyad (ahmedyad200). All rights reserved.**

*This software is provided under a proprietary license. Unauthorized distribution, modification of copyright notices, or resale is strictly prohibited.*

*To use this software, you must purchase a valid license key from the developer. Contact ahmedyad200@gmail.com or @Ayyad on Telegram.*