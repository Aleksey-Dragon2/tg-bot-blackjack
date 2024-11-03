from aiogram import Router
from aiogram.types import CallbackQuery
from config.language import RATING_TEXT, GET_USER_STATS
from database.usersDB import get_rating_users
from bot.markup import RATING_MARKUP, STATS_MARKUP

router = Router()

@router.callback_query(lambda c: c.data == "rating")
async def rating(callback: CallbackQuery):
    if not callback.message:
        return
    await callback.message.edit_text(
        text=RATING_TEXT(get_rating_users()),
        reply_markup=STATS_MARKUP,
        parse_mode="HTML",
    )

@router.callback_query(lambda c: c.data == "stats")
async def stats(callback: CallbackQuery):
    if not callback.message:
        return
    await callback.message.edit_text(
        text=GET_USER_STATS(callback.from_user.id),
        reply_markup=RATING_MARKUP,
        parse_mode="HTML",
    )