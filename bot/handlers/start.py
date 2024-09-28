from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import FIRST_MESSAGE, MAIN, GET_CARD, STOP
from bot.markup import START_MARKUP
from itertools import chain
router = Router()
not_in_game = StateFilter(None)


ALL_COMMANDS = list(chain(MAIN, GET_CARD, STOP))

@router.message(Command("start"), not_in_game)
@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in ALL_COMMANDS], not_in_game)
async def start(message: Message, state: FSMContext):
    await message.answer(
        FIRST_MESSAGE,
        reply_markup=START_MARKUP,
        parse_mode="HTML",
    )