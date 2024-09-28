from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import ADMIN_SUPPORT, check_all_supports
from bot.markup import ADMIN_SUPPORT_MESSAGE_MARKUP
from bot.database import get_all_users_ids
from bot.env import SUPERUSERS
router = Router()

@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT.casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def start(message: Message, state: FSMContext):
    await message.answer(
        check_all_supports(),
        reply_markup=ADMIN_SUPPORT_MESSAGE_MARKUP(get_all_users_ids()),
        parse_mode="HTML",
    )