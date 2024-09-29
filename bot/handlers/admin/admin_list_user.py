from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import ALL_USERS, check_all_users
from bot.markup import ADMIN_MARKUP
from bot.env import SUPERUSERS
router = Router()

@router.message(lambda message: message.text.casefold()==ALL_USERS.casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def start(message: Message, state: FSMContext):
    await message.answer(
        check_all_users(),
        reply_markup=ADMIN_MARKUP,
        parse_mode="HTML",
    )