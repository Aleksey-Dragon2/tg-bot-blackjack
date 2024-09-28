from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import RULES_TEXT, RULES
from bot.markup import START_MARKUP
router = Router()

@router.message(Command("rules"))
@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in RULES])
async def rules(message: Message, state: FSMContext):
    await message.answer(
        RULES_TEXT,
        reply_markup=START_MARKUP,
        parse_mode="HTML",
    )
