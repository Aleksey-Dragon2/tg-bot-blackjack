from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import GET_USER_STATS, STATS
from bot.markup import RATING_MARKUP
router = Router()

@router.message(Command("stats"))
@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in STATS])
async def stats(message: Message, state: FSMContext):
    await message.answer(
        GET_USER_STATS(message.from_user.id),
        reply_markup=RATING_MARKUP,
        parse_mode="HTML",
    )
