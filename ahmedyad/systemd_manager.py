# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import asyncio
import os
from pathlib import Path
from typing import Optional

import aiofiles
import aiofiles.os


class SystemdManager:
    """Manager for systemd services for bot instances"""

    SYSTEMD_PATH = "/etc/systemd/system"

    @staticmethod
    async def create_service(bot_username: str, user_id: int, working_dir: str, venv_path: str = "/root/venv") -> bool:
        """
        Create a systemd service file for a bot instance (async)

        Args:
            bot_username: Bot username (used as service name)
            user_id: User ID who owns the bot
            working_dir: Bot working directory
            venv_path: Path to Python virtual environment

        Returns:
            True if service created successfully, False otherwise
        """
        service_name = f"tgbot-{bot_username}"
        service_file = f"{SystemdManager.SYSTEMD_PATH}/{service_name}.service"

        service_content = f"""[Unit]
Description=Telegram Bot - {bot_username}
After=network.target redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory={working_dir}
Environment="PATH={venv_path}/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart={venv_path}/bin/python3 -B main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

        try:
            # Write service file using aiofiles (async I/O)
            async with aiofiles.open(service_file, 'w') as f:
                await f.write(service_content)

            # Reload systemd daemon
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'daemon-reload',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            # Enable service to start on boot
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'enable', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            # Start service
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'start', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            return True
        except Exception as e:
            print(f"Error creating service {service_name}: {e}")
            return False

    @staticmethod
    async def stop_service(bot_username: str) -> bool:
        """Stop a bot service (async)"""
        service_name = f"tgbot-{bot_username}"
        try:
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'stop', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()
            return True
        except Exception:
            return False

    @staticmethod
    async def start_service(bot_username: str) -> bool:
        """Start a bot service (async)"""
        service_name = f"tgbot-{bot_username}"
        try:
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'start', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()
            return True
        except Exception:
            return False

    @staticmethod
    async def restart_service(bot_username: str) -> bool:
        """Restart a bot service (async)"""
        service_name = f"tgbot-{bot_username}"
        try:
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'restart', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()
            return True
        except Exception:
            return False

    @staticmethod
    async def delete_service(bot_username: str) -> bool:
        """
        Stop, disable, and delete a bot service (async)

        Args:
            bot_username: Bot username

        Returns:
            True if service deleted successfully
        """
        service_name = f"tgbot-{bot_username}"
        service_file = f"{SystemdManager.SYSTEMD_PATH}/{service_name}.service"

        try:
            # Stop service
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'stop', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            # Disable service
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'disable', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            # Remove service file using aiofiles
            if os.path.exists(service_file):
                await aiofiles.os.remove(service_file)

            # Reload systemd daemon
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'daemon-reload',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            # Reset failed state if any
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'reset-failed', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.wait()

            return True
        except Exception as e:
            print(f"Error deleting service {service_name}: {e}")
            return False

    @staticmethod
    def get_service_status(bot_username: str) -> Optional[str]:
        """
        Get service status

        Returns:
            Status string or None if service doesn't exist
        """
        service_name = f"tgbot-{bot_username}"
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception:
            return None

    @staticmethod
    def get_service_logs(bot_username: str, lines: int = 50) -> Optional[str]:
        """
        Get recent logs for a service

        Args:
            bot_username: Bot username
            lines: Number of log lines to retrieve

        Returns:
            Log output or None if error
        """
        service_name = f"tgbot-{bot_username}"
        try:
            result = subprocess.run(
                ['journalctl', '-u', service_name, '-n', str(lines), '--no-pager'],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception:
            return None

    @staticmethod
    def list_bot_services() -> list:
        """
        List all telegram bot services

        Returns:
            List of service names
        """
        try:
            result = subprocess.run(
                ['systemctl', 'list-units', '--type=service', '--all', '--no-pager'],
                capture_output=True,
                text=True
            )

            services = []
            for line in result.stdout.split('\n'):
                if 'tgbot-' in line:
                    parts = line.split()
                    if parts:
                        service_name = parts[0].replace('.service', '')
                        bot_username = service_name.replace('tgbot-', '')
                        services.append(bot_username)

            return services
        except Exception:
            return []

    @staticmethod
    def create_main_bot_service(working_dir: str = "/root", venv_path: str = "/root/venv") -> bool:
        """
        Create systemd service for the main factory bot

        Args:
            working_dir: Main bot working directory
            venv_path: Path to Python virtual environment

        Returns:
            True if service created successfully
        """
        service_name = "tgbot-factory"
        service_file = f"{SystemdManager.SYSTEMD_PATH}/{service_name}.service"

        service_content = f"""[Unit]
Description=Telegram Bot Factory (Main Bot)
After=network.target redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory={working_dir}
Environment="PATH={venv_path}/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart={venv_path}/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

        try:
            # Write service file
            with open(service_file, 'w') as f:
                f.write(service_content)

            # Reload systemd daemon
            subprocess.run(['systemctl', 'daemon-reload'], check=True, capture_output=True)

            # Enable service
            subprocess.run(['systemctl', 'enable', service_name], check=True, capture_output=True)

            # Start service
            subprocess.run(['systemctl', 'start', service_name], check=True, capture_output=True)

            return True
        except Exception as e:
            print(f"Error creating main bot service: {e}")
            return False
