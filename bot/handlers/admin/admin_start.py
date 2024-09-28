from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import ADMNIN_PANEL, SUPERUSER
from bot.markup import SUPERUSER_MARKUP
from bot.env import SUPERUSERS
router = Router()

@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in SUPERUSER] and message.from_user.id in [int(user) for user in SUPERUSERS])
async def start(message: Message, state: FSMContext):
    await message.answer(
        ADMNIN_PANEL,
        reply_markup=SUPERUSER_MARKUP,
        parse_mode="HTML",
    )