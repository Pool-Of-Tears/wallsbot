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

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)

import shortuuid
from wallsbot import dp, BOT_ADMINS
from wallsbot.utils.wall import Wall, CATEGORIES


class Submissions:
    def __init__(self):
        self.submissions = {}

    def submit(self, wall: Wall):
        submission_id = shortuuid.uuid()
        self.submissions[submission_id] = wall
        self._notify_admins(submission_id, wall)

    def get(self, submission_id):
        try:
            return self.submissions.pop(submission_id)
        except KeyError:
            return None

    @staticmethod
    def _notify_admins(submission_id, wall):
        caption = "New submission ✨"
        caption += f"Submitted by {wall.submitter.mention_html()}\n"
        caption += f"Category : {wall.category}\n"
        caption += f"Tags : {wall.tags}\n"

        for admin in BOT_ADMINS:
            dp.bot.send_photo(
                admin,
                wall.photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Approve ✅",
                                callback_data=f"approveWall_yes_{submission_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Disapprove ❌",
                                callback_data=f"approveWall_no_{submission_id}",
                            )
                        ],
                    ]
                ),
            )


SUBMISSIONS = Submissions()
ENTER_TAGS, ENTER_WALL, PROCESS_WALL = range(3)

# =========================================================#
# submission handler
# =========================================================#


def start_submission(update: Update, context: CallbackContext) -> int:
    context.user_data["submission"] = {}
    text = (
        "So you want to submit a wallpaper? Great! "
        "Please choose the wallpaper category."
    )
    reply_keyboard = []
    # insert a lists including two items in each.
    it = iter(CATEGORIES)
    for x in it:
        reply_keyboard.append([x, next(it)])

    msg = update.effective_message
    msg.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            selective=True,
            resize_keyboard=True,
        ),
    )

    return ENTER_TAGS


def choose_tags(update: Update, context: CallbackContext) -> int:
    msg = update.effective_message
    if msg.text in CATEGORIES:
        context.user_data["submission"]["category"] = msg.text
        text = (
            "Nice! now enter some tags with single space "
            "between them, for example if you're posting a "
            "nature wallpaper which contains trees ane birds "
            "then tags would be: <i>nature trees birds</i> "
            "etc...\nYou can use max 7 tags."
        )
        msg.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return ENTER_WALL
    else:
        msg.reply_text(
            "Sorry, you've chosen an invalid category please try again.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END


def enter_wall(update: Update, context: CallbackContext) -> int:
    msg = update.effective_message
    context.user_data["submission"]["tags"] = msg.text.split(" ")[:7]
    msg.reply_text("Okay now send the wallpaper as document.")
    return PROCESS_WALL


def process_wall(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    msg = update.effective_message

    file = msg.document.get_file()
    context.user_data["submission"]["file"] = file

    try:
        rep = msg.reply_text("Processing . . .")
        wall = Wall(submitter=user, **context.user_data["submission"])
    except IOError:
        rep.edit_text(
            "Sorry this looks like an invalid file "
            "format, Please try again."
        )
        return ConversationHandler.END

    if user.id in BOT_ADMINS:
        post_link = wall.post_into_channel()
        rep.edit_text(
            "Sucessfully posted wallpaper in the channel.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Post link  🔗", url=post_link)]]
            ),
        )

    else:
        SUBMISSIONS.submit(wall)
        context.user_data.clear()
        rep.edit_text(
            "Thanks! your wallpaper is sucessfully submitted and is "
            "currently waiting for approval, i'll notify you once it "
            "gets approved or unapproved."
        )
    return ConversationHandler.END


def cancel_conv(update: Update, _) -> int:
    update.effective_message.reply_text("Cancelled!")
    return ConversationHandler.END


def conv_timeout(update: Update, _) -> int:
    update.effective_message.reply_text(
        "Didn't got any response within specified time, cancelling..."
    )


# =========================================================#
# Approval handler
# =========================================================#


def approve_wall(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer("Hold on...")

    status, submission_id = query.data.split("_")[1:]
    submission = SUBMISSIONS.get(submission_id)
    if submission is None:
        query.edit_message_caption(
            "This submission is already reviewed by other admin."
        )
        return

    if status == "yes":
        post_link = submission.post_into_channel()
        query.edit_message_caption(
            "Done! I've posted this wallpaper in the channel.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Post link  🔗", url=post_link)]]
            ),
        )
        submission.submitter.send_message(
            "The wallpaper you had submitted is approved "
            "by the admin and sucessfully posted to the channel.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Post link  🔗", url=post_link)]]
            ),
        )

    else:
        query.edit_message_caption(
            "Okay I've notified the submitter about unapproval."
        )
        submission.submitter.send_message(
            "Sorry, the wallpaper you've submitted couldn't be approved."
        )


# =========================================================#
# Handlers
# =========================================================#

SUBMIT_WALL_HANDLER = ConversationHandler(
    entry_points=[CommandHandler(["submit", "post"], start_submission)],
    states={
        ENTER_TAGS: [
            MessageHandler(Filters.text & ~Filters.command, choose_tags)
        ],
        ENTER_WALL: [
            MessageHandler(Filters.text & ~Filters.command, enter_wall)
        ],
        PROCESS_WALL: [
            MessageHandler(
                Filters.document,
                process_wall,
            )
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(Filters.all, conv_timeout)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_conv)],
    conversation_timeout=100,
)

APPROVAL_HANDLER = CallbackQueryHandler(approve_wall, pattern=r"approveWall_")

dp.add_handler(SUBMIT_WALL_HANDLER)
dp.add_handler(APPROVAL_HANDLER)
