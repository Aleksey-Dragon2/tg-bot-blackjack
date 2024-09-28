from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import COMMAND_NOT_FOUND
from bot.handlers.start import start
import asyncio

router = Router()

@router.message(lambda message: True)
async def handle_unregistered_messages(message: Message, state: FSMContext):
    await message.answer(COMMAND_NOT_FOUND, parse_mode="HTML")
    await asyncio.sleep(300 / 1000) 
    await start(message, state)