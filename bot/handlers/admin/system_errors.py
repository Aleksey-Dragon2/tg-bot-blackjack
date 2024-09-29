from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import ERRORS, ADMIN_ERROR_LOG
from bot.markup import ADMIN_MARKUP
from bot.env import SUPERUSERS
from database.ErrorLogDB import get_error_log

router = Router()

@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in ERRORS] and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_panel(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_ERROR_LOG(get_error_log()),
        reply_markup=ADMIN_MARKUP,
        parse_mode="HTML",
    )