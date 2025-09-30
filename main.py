#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный файл для запуска CLI инструмента Yandex Tracker.
Учитывает особенности кодировки для PowerShell и Windows.
"""

import sys
import os

# Устанавливаем кодировку для корректного вывода в PowerShell
if sys.platform == 'win32':
    # Для Windows устанавливаем UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Также можно попробовать sys.stdout.reconfigure(encoding='utf-8')

# Импортируем и запускаем CLI
from src.cli import cli

if __name__ == '__main__':
    cli()