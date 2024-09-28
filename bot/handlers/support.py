from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config.language import SUPPORT, HELP_SUPPORT, SEND_SUPPORT_MESSAGE, SUPPORT_MESSAGE, SUPPORT_MESSAGE_SENT, SUPPORT_MESSAGE_DENIED, SUPPORT_MESSAGE_CONFIRMATION
from config.language import SUPPORT_INVALID_MOVE, SUPPORT_BACK, USER_SUPPORT_MESSAGES, SEND_USER_SUPPORT_MESSAGES
from bot.markup import SUPPORT_MARKUP, CONFIRM_SUPPORT_MARKUP
from bot.FSM import GameState
from database.supports import add_support_message, get_all_support_message_user
from bot.handlers.start import start
import asyncio

router = Router()

@router.message(Command("support"))
@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in SUPPORT])
async def stats(message: Message, state: FSMContext):
    await state.set_state(GameState.CHOOSING_SUPPORT)
    await message.answer(
        HELP_SUPPORT,
        reply_markup=SUPPORT_MARKUP,
        parse_mode="HTML",
    )

@router.message(GameState.CHOOSING_SUPPORT, lambda message: message.text.casefold() in [cmd.casefold() for cmd in SEND_SUPPORT_MESSAGE])
async def process_support_choice(message: Message, state: FSMContext):
    await state.set_state(GameState.SUPPORT_MESSAGE)
    await message.answer(SUPPORT_MESSAGE)

@router.message(GameState.CHOOSING_SUPPORT, lambda message: message.text.casefold() in [cmd.casefold() for cmd in SUPPORT_BACK])
async def process_support_back(message: Message, state: FSMContext):
    await state.clear()
    await start(message, state)

@router.message(GameState.CHOOSING_SUPPORT, lambda message: message.text.casefold() in [cmd.casefold() for cmd in USER_SUPPORT_MESSAGES])
async def process_user_support_messages(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    else:
        id=message.from_user.id
    await message.answer(
        SEND_USER_SUPPORT_MESSAGES(get_all_support_message_user(id)),
        parse_mode="HTML",
    )

@router.message(GameState.SUPPORT_MESSAGE)
async def process_support_message(message: Message, state: FSMContext):
    text_message=str(message.text)
    await state.update_data(text_message=text_message)
    await message.answer(
        SUPPORT_MESSAGE_CONFIRMATION(text_message),
        reply_markup=CONFIRM_SUPPORT_MARKUP,
        parse_mode="HTML",
    )
    await state.set_state(GameState.CONFIRM_SUPPORT_MESSAGE)

@router.callback_query(GameState.CONFIRM_SUPPORT_MESSAGE, lambda c: c.data == "confirm_support")
async def confirm_support(callback: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    text_message=str(data['text_message'])

    add_support_message(callback.from_user.id, callback.from_user.username, callback.from_user.first_name, text_message)
    await callback.message.edit_text(text=SUPPORT_MESSAGE_SENT(text_message))
    await state.clear()
    await asyncio.sleep(500/1000)
    await start(callback.message, state)

@router.callback_query(GameState.CONFIRM_SUPPORT_MESSAGE, lambda c: c.data == "deny_support")
async def deny_support(callback: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    text_message=str(data['text_message'])
    await callback.message.edit_text(text=SUPPORT_MESSAGE_DENIED(text_message))
    await asyncio.sleep(500/1000)
    await start(callback.message, state)
    await state.clear()

@router.message(GameState.CHOOSING_SUPPORT)
async def handle_invalid_action(message: Message, state: FSMContext):
    await message.answer(SUPPORT_INVALID_MOVE)