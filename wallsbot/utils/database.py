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
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, BigInteger, String

from wallsbot import DB_URI


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()


class Wallpaper(BASE):
    __tablename__ = "wallpaper"
    submitter_id = Column(BigInteger, primary_key=True)
    category = Column(String, primary_key=True)
    file_id = Column(String, primary_key=True)
    message_id = Column(BigInteger)

    def __init__(self, submitter_id, category, file_id, message_id):
        self.submitter_id = submitter_id
        self.category = category
        self.file_id = file_id
        self.message_id = message_id

    def __repr__(self):
        repr_text = f"{self.__class__.__name__}("
        repr_text += f"submitter_id={self.submitter_id}, "
        repr_text += f"category={self.category}, "
        repr_text += f"file_id={self.file_id}, "
        repr_text += f"message_id={self.message_id})"
        return repr_text


Wallpaper.__table__.create(checkfirst=True)


def insert_wall(*args, **kwargs):
    SESSION.merge(Wallpaper(*args, **kwargs))
    SESSION.commit()


def walls_by_category(category):
    try:
        walls = (
            SESSION.query(Wallpaper)
            .filter(Wallpaper.category == category)
            .all()
        )
        return walls
    finally:
        SESSION.close()


def wall_by_user(user_id):
    try:
        walls = (
            SESSION.query(Wallpaper)
            .filter(Wallpaper.submitter_id == user_id)
            .all()
        )
        return walls
    finally:
        SESSION.close()
