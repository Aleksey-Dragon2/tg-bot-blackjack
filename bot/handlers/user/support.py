from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config.language import SUPPORT, HELP_SUPPORT, SEND_SUPPORT_MESSAGE, SUPPORT_MESSAGE, SUPPORT_MESSAGE_SENT, SUPPORT_MESSAGE_DENIED, SUPPORT_MESSAGE_CONFIRMATION
from config.language import SUPPORT_INVALID_MOVE, SUPPORT_BACK, USER_SUPPORT_MESSAGES, SEND_USER_SUPPORT_MESSAGES
from bot.markup import SUPPORT_MARKUP, CONFIRM_SUPPORT_MARKUP, PAGINATION_MARKUP
from bot.FSM import GameState
from database.supportsDB import add_support_message, get_all_support_message_user
from bot.handlers.user.start import start
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

## SEND_SUPPORT_MESSAGE
@router.message(GameState.CHOOSING_SUPPORT, lambda message: message.text.casefold() in [cmd.casefold() for cmd in SEND_SUPPORT_MESSAGE])
async def process_support_choice(message: Message, state: FSMContext):
    await state.set_state(GameState.SUPPORT_MESSAGE)
    await message.answer(SUPPORT_MESSAGE)

## BACK
@router.message(GameState.CHOOSING_SUPPORT, lambda message: message.text.casefold() in [cmd.casefold() for cmd in SUPPORT_BACK])
async def process_support_back(message: Message, state: FSMContext):
    await state.clear()
    await start(message, state)

## ALL_MESSAGES
@router.message(GameState.CHOOSING_SUPPORT, lambda message: message.text.casefold() in [cmd.casefold() for cmd in USER_SUPPORT_MESSAGES])
async def process_user_support_messages(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    else:
        user_id = message.from_user.id
    
    supports = get_all_support_message_user(user_id)
    total_pages = (len(supports)+4) // 5  # supports+4
    await state.update_data(page=0, supports=supports)
    
    await message.answer(
        SEND_USER_SUPPORT_MESSAGES(supports, page=0),
        reply_markup=PAGINATION_MARKUP(0, total_pages),
        parse_mode="HTML",
    )

## GET_SUPPORT_MESSAGE
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

## CONFIRM_SUPPORT_MESSAGE
@router.callback_query(GameState.CONFIRM_SUPPORT_MESSAGE, lambda c: c.data == "confirm_support")
async def confirm_support(callback: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    text_message=str(data['text_message'])

    add_support_message(callback.from_user.id, callback.from_user.username, callback.from_user.first_name, text_message)
    await callback.message.edit_text(text=SUPPORT_MESSAGE_SENT(text_message))
    await state.clear()
    await asyncio.sleep(500/1000)
    await start(callback.message, state)

## DENY_SUPPORT_MESSAGE
@router.callback_query(GameState.CONFIRM_SUPPORT_MESSAGE, lambda c: c.data == "deny_support")
async def deny_support(callback: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    text_message=str(data['text_message'])
    await callback.message.edit_text(text=SUPPORT_MESSAGE_DENIED(text_message))
    await asyncio.sleep(500/1000)
    await start(callback.message, state)
    await state.clear()

## CHOOSING_SUPPORT ACTION
@router.message(GameState.CHOOSING_SUPPORT)
async def handle_invalid_action(message: Message, state: FSMContext):
    await message.answer(SUPPORT_INVALID_MOVE)

@router.callback_query(lambda c: c.data.startswith("page_"))
async def paginate_support_messages(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[1])
    data = await state.get_data()
    supports = data['supports']
    total_pages = (len(supports)+4) // 5  # Calculate total pages
    
    await callback.message.edit_text(
        SEND_USER_SUPPORT_MESSAGES(supports, page=page),
        reply_markup=PAGINATION_MARKUP(page, total_pages),
        parse_mode="HTML",
    )
    await state.update_data(page=page)