from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config.language import ERRORS, ADMIN_ERROR_LOG
from bot.markup import ERROR_RESET_MARKUP
from bot.env import SUPERUSERS
from database.ErrorLogDB import get_error_log, clear_error_log

router = Router()

@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in ERRORS] and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_panel(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_ERROR_LOG(get_error_log()),
        reply_markup=ERROR_RESET_MARKUP,
        parse_mode="HTML",
    )

@router.callback_query(lambda c: c.data == "error_reset")
async def reset_error_log(callback: CallbackQuery):
    clear_error_log()
    if callback.message is None:
        return
    await callback.message.edit_text(text=ADMIN_ERROR_LOG(get_error_log()))