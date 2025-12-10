#!/bin/bash

# ---------------------- المتغيرات ----------------------

# وضع non-interactive لتثبيت الحزم
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a

# ألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# مسارات وملفات
VENV_PATH="/root/venv"
REQUIREMENTS_FILE="/root/requirements.txt"
PYTHON_SCRIPT="/root/main.py"
SERVICE_NAME="tgbot-factory"
BASHRC="/root/.bashrc"
INFO_FILE="/root/info.py"
REPO_URL="https://github.com/ahmedayyad-dev/EHkBot.git"

# ---------------------- التحقق من الصلاحيات ----------------------

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root using sudo!${RESET}"
    exit 1
fi

# التحقق من إصدار ديبيان
if [ -f /etc/debian_version ]; then
    DEBIAN_VERSION=$(cat /etc/debian_version)
    if [[ "$DEBIAN_VERSION" =~ ^([0-9]+) ]]; then
        DEBIAN_MAJOR_VERSION=${BASH_REMATCH[1]}
        echo -e "${BLUE}Detected Debian version: $DEBIAN_VERSION${RESET}"
    fi
fi

# ---------------------- تحديث النظام وتثبيت الحزم ----------------------

echo -e "${CYAN}Updating and upgrading system...${RESET}"
apt update && apt full-upgrade -y
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to update system. Please check your internet connection.${RESET}"
    exit 1
fi

echo -e "${CYAN}Installing build dependencies...${RESET}"
apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev redis-server ffmpeg unzip
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies.${RESET}"
    exit 1
fi

echo ""

# ---------------------- جمع معلومات info.py ----------------------

echo -e "${CYAN}==================================================================${RESET}"
echo -e "${GREEN}       Welcome to Telegram Bot Factory Installation       ${RESET}"
echo -e "${CYAN}==================================================================${RESET}"
echo ""

if [ -f "$INFO_FILE" ]; then
    echo -e "${GREEN}Found existing info.py. Using saved credentials...${RESET}"
    echo ""
else
    echo -e "${YELLOW}Please provide the following information to configure your bot:${RESET}"
    echo ""

    echo -e "${CYAN}Enter your Bot Token (from @BotFather):${RESET}"
    read -p "> " FBOT_TOKEN

    echo -e "${CYAN}Enter your Telegram User ID:${RESET}"
    read -p "> " OWNER_ID

    echo -e "${CYAN}Enter your RapidAPI Key:${RESET}"
    echo -e "${YELLOW}(Subscribe at: https://rapidapi.com/ahmedyad200/api/youtube-to-telegram-uploader-api)${RESET}"
    read -p "> " RAPIDAPI_KEY

    echo -e "${CYAN}Enter your License Key:${RESET}"
    echo -e "${YELLOW}(Contact: ahmedyad200@gmail.com or @Ayyad on Telegram)${RESET}"
    read -p "> " LICENSE_KEY

    echo -e "${CYAN}Enter your Telegram Channel username (without @):${RESET}"
    read -p "> " CHANNEL
    CHANNEL=$(echo "$CHANNEL" | sed 's/@//g')

    echo -e "${CYAN}Enter your API ID (from my.telegram.org):${RESET}"
    read -p "> " API_ID

    echo -e "${CYAN}Enter your API Hash (from my.telegram.org):${RESET}"
    read -p "> " API_HASH

    echo ""
    echo -e "${GREEN}✓ All information collected successfully!${RESET}"
    echo ""
fi

# ---------------------- Clone المشروع ----------------------

echo -e "${CYAN}Cloning project from GitHub...${RESET}"
cd /root

# إنشاء مجلد مؤقت للـ clone
TEMP_DIR="/tmp/bot_temp_$$"
git clone $REPO_URL $TEMP_DIR

echo -e "${CYAN}Copying files to /root/...${RESET}"
# نسخ كل الملفات من المجلد المؤقت (يستبدل أي ملفات موجودة)
cp -rf $TEMP_DIR/. /root/

# حذف المجلد المؤقت
rm -rf $TEMP_DIR

echo -e "${GREEN}✓ Project files copied successfully!${RESET}"
echo ""

# ---------------------- Clone Template Bot ----------------------

echo -e "${CYAN}Cloning Template Bot...${RESET}"
cd /root
git clone https://github.com/ahmedayyad-dev/Template-Bot-for-EHkBot ahmedyad200
echo -e "${GREEN}✓ Template Bot cloned successfully!${RESET}"
echo ""

# ---------------------- إنشاء ملف info.py ----------------------

echo -e "${CYAN}Creating info.py configuration file...${RESET}"
cat > $INFO_FILE << EOF
# info.py - Bot Configuration
# Copyright © 2025 Ahmed Ayyad (ahmedyad200). All rights reserved.

FBotToken = '$FBOT_TOKEN'
owner_id = $OWNER_ID
rapidapi_key = '$RAPIDAPI_KEY'
LICENSE_KEY = '$LICENSE_KEY'
channel = '$CHANNEL'
api_id = $API_ID
api_hash = '$API_HASH'
EOF

echo -e "${GREEN}✓ info.py created successfully!${RESET}"
echo ""

# ---------------------- تثبيت pyenv ----------------------

echo -e "${CYAN}Installing pyenv...${RESET}"
if [ ! -d "$HOME/.pyenv" ]; then
    curl -fsSL https://pyenv.run | bash
    echo -e "${GREEN}pyenv installed successfully!${RESET}"
else
    echo -e "${YELLOW}pyenv already installed, skipping...${RESET}"
fi

# إعداد pyenv في البيئة الحالية
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# إضافة pyenv للـ bashrc إذا لم يكن موجوداً
if ! grep -q 'PYENV_ROOT' $BASHRC; then
    echo -e "${CYAN}Adding pyenv to .bashrc...${RESET}"
    cat << 'EOF' >> $BASHRC

# pyenv configuration
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
EOF
fi

# ---------------------- تثبيت Python 3.10.12 باستخدام pyenv ----------------------

echo -e "${CYAN}Installing Python 3.10.12 using pyenv...${RESET}"
echo -e "${YELLOW}This may take 5-10 minutes, please wait...${RESET}"

if pyenv versions | grep -q "3.10.12"; then
    echo -e "${YELLOW}Python 3.10.12 already installed via pyenv, skipping...${RESET}"
else
    pyenv install 3.10.12
    echo -e "${GREEN}Python 3.10.12 installed successfully!${RESET}"
fi

# التحقق من تثبيت Python 3.10.12
PYTHON_BINARY="$PYENV_ROOT/versions/3.10.12/bin/python3"
if [ -f "$PYTHON_BINARY" ]; then
    INSTALLED_VERSION=$($PYTHON_BINARY --version)
    echo -e "${GREEN}$INSTALLED_VERSION installed successfully!${RESET}"
else
    echo -e "${RED}Failed to install Python 3.10.12${RESET}"
    exit 1
fi

# ---------------------- إعداد البيئة الافتراضية ----------------------

echo -e "${CYAN}Creating virtual environment at $VENV_PATH using Python 3.10.12...${RESET}"
$PYTHON_BINARY -m venv $VENV_PATH

echo -e "${CYAN}Activating virtual environment...${RESET}"
source $VENV_PATH/bin/activate

# التحقق من إصدار Python داخل البيئة الافتراضية
VENV_PYTHON_VERSION=$(python --version)
echo -e "${GREEN}Virtual environment is using: $VENV_PYTHON_VERSION${RESET}"

# ---------------------- تثبيت المكتبات من requirements.txt ----------------------

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo -e "${CYAN}Installing Python packages from $REQUIREMENTS_FILE...${RESET}"
    pip install --upgrade pip
    pip install -r $REQUIREMENTS_FILE
    echo -e "${GREEN}Python packages installed successfully!${RESET}"
else
    echo -e "${YELLOW}Warning: $REQUIREMENTS_FILE not found. Skipping package installation.${RESET}"
fi

# ---------------------- تفعيل البيئة الافتراضية تلقائيًا عند تسجيل الدخول ----------------------

echo -e "${CYAN}Configuring auto-activation of virtual environment for root...${RESET}"

# إزالة أي إعدادات قديمة للبيئة الافتراضية من .bashrc
sed -i '/# Auto-activate virtual environment/d' $BASHRC
sed -i '\|source /root/venv/bin/activate|d' $BASHRC

# إضافة تفعيل تلقائي للبيئة الافتراضية
cat << 'EOF' >> $BASHRC

# Auto-activate virtual environment
if [ -d "/root/venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    source /root/venv/bin/activate
fi
EOF

echo -e "${GREEN}Virtual environment will auto-activate on SSH login for root!${RESET}"

# ---------------------- إنشاء وتشغيل systemd service ----------------------

echo -e "${CYAN}Creating systemd service '$SERVICE_NAME' and starting main bot...${RESET}"

# التحقق من وجود main.py
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${YELLOW}Warning: $PYTHON_SCRIPT not found. Service will be created but won't run properly.${RESET}"
fi

# إنشاء ملف systemd service
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Telegram Bot Factory (Main Bot)
After=network.target redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/root
Environment="PATH=$VENV_PATH/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$VENV_PATH/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# إعادة تحميل systemd daemon
systemctl daemon-reload

# تفعيل وتشغيل الخدمة
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo -e "${GREEN}Systemd service '$SERVICE_NAME' created and started successfully!${RESET}"
echo -e "${BLUE}To view logs, use: journalctl -u $SERVICE_NAME -f${RESET}"
echo -e "${BLUE}To check status, use: systemctl status $SERVICE_NAME${RESET}"

# ---------------------- النهاية ----------------------
echo ""
echo -e "${CYAN}==================================================================${RESET}"
echo -e "${GREEN}Setup completed successfully!${RESET}"
echo -e "${CYAN}==================================================================${RESET}"
echo -e "${CYAN}Virtual environment: $VENV_PATH${RESET}"
echo -e "${CYAN}Python version in venv: $VENV_PYTHON_VERSION${RESET}"
echo -e "${CYAN}Systemd service: $SERVICE_NAME${RESET}"
echo -e "${CYAN}Configuration file: $INFO_FILE${RESET}"
echo ""
echo -e "${GREEN}Your bot is now running!${RESET}"
echo -e "${YELLOW}Useful commands:${RESET}"
echo -e "  ${BLUE}systemctl status $SERVICE_NAME${RESET}     - Check bot status"
echo -e "  ${BLUE}journalctl -u $SERVICE_NAME -f${RESET}     - View live logs"
echo -e "  ${BLUE}systemctl restart $SERVICE_NAME${RESET}    - Restart bot"
echo -e "  ${BLUE}systemctl stop $SERVICE_NAME${RESET}       - Stop bot"
echo ""