# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Stɑrry Shivɑm
#
# Permission is hereby granted, free of charg>
# of this software and associated documentati>
# in the Software without restriction, includ>
# to use, copy, modify, merge, publish, distr>
# copies of the Software, and to permit perso>
# furnished to do so, subject to the followin>
#
# The above copyright notice and this permiss>
# copies or substantial portions of the Softw>
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT W>
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE W>
# FITNESS FOR A PARTICULAR PURPOSE AND NONINF>
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR >
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT>
# OUT OF OR IN CONNECTION WITH THE SOFTWARE O>
# SOFTWARE.

import logging
import importlib

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CommandHandler, TypeHandler, DispatcherHandlerStop

from wallsbot import updater, dp, CHANNEL_ID
from wallsbot.plugins import PLUGINS

# load all plugins
for x in PLUGINS:
    importlib.import_module("wallsbot.plugins." + x)

logger = logging.getLogger(__name__)


def start(update: Update, _) -> None:
    message = update.effective_message
    message.reply_text(f"Hello {message.from_user.first_name}")


def chat_checker(update: Update, _) -> None:
    user = update.effective_user
    message = update.effective_message

    not_in_chat = False
    try:
        chatmem = dp.bot.get_chat_member(CHANNEL_ID, user.id)
    except BadRequest:
        not_in_chat = True

    if not_in_chat or chatmem.status in {"kicked", "left"}:
        message.reply_text(
            "Sorry! you need to join @StarryWalls before using me."
        )
        raise DispatcherHandlerStop()


def main() -> None:
    chat_checker_handler = TypeHandler(Update, chat_checker, run_async=False)
    start_handler = CommandHandler("start", start)

    dp.add_handler(chat_checker_handler, -10)
    dp.add_handler(start_handler)

    logger.info("Starting %s using polling", dp.bot.first_name)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
