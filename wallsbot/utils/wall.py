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
from io import BytesIO
from telegram import User, File

from wallsbot import dp, CHANNEL_ID
import wallsbot.utils.database as db


CATEGORIES = [
    "Abstract",
    "Animals",
    "Anime",
    "Brands",
    "Cars",
    "Cartoon",
    "Celebrities",
    "Devices",
    "Games",
    "Geography",
    "Graphics",
    "Minimal",
    "Movies",
    "Music",
    "Nature",
    "Other",
    "Space",
    "Sports",
    "SuperHeros",
    "TV Shows",
]


class Wall:
    def __init__(
        self,
        file: File,
        tags: list,
        category: str,
        submitter: User,
    ):
        self.file = file
        self.tags = self._build_tags(tags)
        self.category = category
        self.submitter = submitter

        self.photo = self._build_photo(file)

    @staticmethod
    def _build_tags(tags: list):
        ret = ""
        for x in tags:
            ret += f"#{x} "
        return ret

    @staticmethod
    def _build_photo(file: File):
        bytes_io = BytesIO()
        file.download(out=bytes_io)
        return bytes_io.getvalue()

    def _insert_into_db(self, message):
        db.insert_wall(
            submitter_id=self.submitter.id,
            category=self.category,
            file_id=self.file.file_id,
            message_id=message.message_id,
        )

    def post_into_channel(self):
        caption = f"<b>×</b> Category : {self.category}\n"
        caption += f"<b>×</b> Tags : {self.tags}\n"
        caption += f"<b>×</b> Posted by {self.submitter.mention_html()}"
        dp.bot.send_photo(CHANNEL_ID, photo=self.photo, caption=caption)
        msg = dp.bot.send_document(
            CHANNEL_ID, document=self.photo, filename="@StarryWalls.png"
        )
        self._insert_into_db(msg)
        return msg.link
