# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Stɑrry Shivɑm
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import logging

import telegram.ext as tg
from telegram import ParseMode
from dotenv import load_dotenv


__author__ = "Stɑrry Shivɑm <starry369126@outlook.com"
__license__ = "MIT License <https://opensource.org/licenses/MIT>"
__copyright__ = "2021 Stɑrry Shivɑm <https://github.com/starry69>"


# Check python version:
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    print("==================================")
    print("You MUST need to have python version 3.9! shutting down...")
    print("==================================")
    sys.exit(1)

# load env file if present:
load_dotenv("./config.env")

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))
BOT_ADMINS = {int(x) for x in os.environ.get("BOT_ADMINS", "0").split()}
DB_URI = os.environ.get("DATABASE_URL")
DEBUG = bool(os.environ.get("DEBUG", False))

# set logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG if DEBUG is True else logging.INFO,
)

# set Defaults and updater
defaults = tg.Defaults(timeout=100, run_async=True, parse_mode=ParseMode.HTML)
updater = tg.Updater(
    TOKEN,
    workers=min(32, os.cpu_count() + 4),
    defaults=defaults,
    request_kwargs={"read_timeout": 10, "connect_timeout": 10},
)

# assign dispatcher
dp = updater.dispatcher
