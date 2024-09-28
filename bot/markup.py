import config.language as lang

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


START_MARKUP = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=lang.START_GAME), KeyboardButton(text=lang.STATS[0])],
        [
            KeyboardButton(text=lang.RULES[0]),
            KeyboardButton(text=lang.SUPPORT[0]),
        ],
    ],
)


GAME_MARKUP = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=lang.GET_CARD[0]), KeyboardButton(text=lang.STOP[0])],
        ],
    )

RESTART_MARKUP = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=lang.RESTART)],
        [KeyboardButton(text=lang.MAIN[0])],
    ],
)


SUPPORT_MARKUP = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=lang.SEND_SUPPORT_MESSAGE[0]), KeyboardButton(text=lang.SUPPORT_BACK[0])],
        [KeyboardButton(text=lang.USER_SUPPORT_MESSAGES[0])],
    ],
)

CONFIRM_SUPPORT_MARKUP = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=lang.CONFIRM_SUPPORT_MESSAGE[0], callback_data="confirm_support"),
         InlineKeyboardButton(text=lang.DENY_SUPPORT_MESSAGE[0], callback_data="deny_support")],
    ],
)

SUPERUSER_MARKUP = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=lang.ALL_USERS), KeyboardButton(text=lang.ADMIN_SUPPORT_LIST)],
        [KeyboardButton(text=lang.SEND_MESSAGE_ALL[0])],
    ],
)

ADMIN_SUPPORT_LIST_MARKUP = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=lang.ADMIN_SUPPORT_RELEVANT_LIST[0]), KeyboardButton(text=lang.ADMIN_SUPPORT_ARCHIVE_LIST[0])],
        [KeyboardButton(text=lang.ADMIN_SUPPORT_MENU_BACK[0])],
    ],
)

def ADMIN_SUPPORT_MESSAGES_MARKUPS(ids):
    action='help'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(id), callback_data=f"{action}_{str(id)}") for id in ids[i:i+3]] for i in range(0, len(ids), 3)
    ])
    return keyboard

def ADMIN_SUPPORT_MENU_MARKUP(support_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang.ADMIN_SUPPORT_MENU_CONFIRM[0], callback_data=f"admin_support_confirm_{support_id}"),
        InlineKeyboardButton(text=lang.ADMIN_SUPPORT_MENU_DENY[0], callback_data=f"admin_support_deny_{support_id}")],

        [InlineKeyboardButton(text=lang.ADMIN_SUPPORT_MENU_BACK[0], callback_data=f"admin_support_back_{support_id}")],
    ],
)
    return keyboard

ADMIN_SEND_MESSAGE_ALL_MARKUP = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=lang.CONFIRM_SEND_MESSAGE_ALL[0], callback_data="confirm_send_message_all"),
        InlineKeyboardButton(text=lang.DENY_SEND_MESSAGE_ALL[0], callback_data="deny_send_message_all")],
    ],
)