from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config.language import SEND_MESSAGE_ALL, ADMIN_SEND_ALL_MESSAGE, SEND_MESSAGE_ALL_CONFIRMATION, SEND_MESSAGE_ALL_SENT, SEND_MESSAGE_ALL_DENIED
from bot.env import SUPERUSERS
from bot.FSM import AdminState
from bot.markup import ADMIN_SEND_MESSAGE_ALL_MARKUP
from database.users import get_users_ids
from bot.client import bot
router = Router()

@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in SEND_MESSAGE_ALL] and message.from_user.id in [int(user) for user in SUPERUSERS])
async def inform_all(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_SEND_ALL_MESSAGE,
        parse_mode="HTML",
    )
    await state.set_state(AdminState.SENDING_MESSAGE_ALL)

@router.message(AdminState.SENDING_MESSAGE_ALL)
async def process_message(message: Message, state: FSMContext):
    text_message=str(message.text)
    await state.update_data(text_message=text_message)
    await message.answer(
        SEND_MESSAGE_ALL_CONFIRMATION(text_message),
        reply_markup=ADMIN_SEND_MESSAGE_ALL_MARKUP,
        parse_mode="HTML",
    )
    await state.set_state(AdminState.AWAITING_CONFIRMATION)

@router.callback_query(AdminState.AWAITING_CONFIRMATION, lambda c: c.data == "confirm_send_message_all")
async def confirm_send_message_all(callback: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    text_message=str(data['text_message'])
    await callback.message.edit_text(text=SEND_MESSAGE_ALL_SENT(text_message))
    for user in get_users_ids():
        await bot.send_message(chat_id=user, text=text_message)
    await state.clear()

@router.callback_query(AdminState.AWAITING_CONFIRMATION, lambda c: c.data == "deny_send_message_all")
async def deny_send_message_all(callback: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    text_message=str(data['text_message'])
    await callback.message.edit_text(text=SEND_MESSAGE_ALL_DENIED(text_message))
    await state.clear()