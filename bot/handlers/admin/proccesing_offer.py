from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.language import ADMIN_MESSAGE_PROCESSED,check_all_supports
from bot.markup import ADMIN_SUPPORT_MESSAGES_MARKUPS

from database.supportsDB import get_all_support_ids, check_support_messages, get_support_user_id
from database.archive_supportDB import move_support_to_archive

from bot.client import bot
import asyncio
from bot.env import SUPERUSERS
router = Router()

## Подтверждение предложения
@router.callback_query(lambda c: c.data.startswith("admin_support_confirm_"))
async def admin_support_confirm(callback: CallbackQuery, state: FSMContext):
    support_id=callback.data.split("_")[3]
    user_id=get_support_user_id(support_id)
    move_support_to_archive(support_id, 'Accepted')
    if not callback.message:
        return
    await callback.message.edit_text(
        ADMIN_MESSAGE_PROCESSED
    )
    await bot.send_message(chat_id=user_id, text=f"Ваше предложение {support_id} было принято")
    await asyncio.sleep(500/1000)
    await admin_support_back(callback, state)

## Отклонение предложения
@router.callback_query(lambda c: c.data.startswith("admin_support_deny_"))
async def admin_support_deny(callback: CallbackQuery, state: FSMContext):
    support_id=callback.data.split("_")[3]
    user_id=get_support_user_id(support_id)
    move_support_to_archive(support_id, 'Denied')
    if not callback.message:
        return
    await callback.message.edit_text(
        ADMIN_MESSAGE_PROCESSED
    )
    await bot.send_message(chat_id=user_id, text=f"Ваше предложение {support_id} было отклонено")
    await asyncio.sleep(500/1000)
    await admin_support_back(callback, state)

## Возвращение назад к выборы списка предложений
@router.callback_query(lambda c: c.data.startswith("admin_support_back_"))
async def admin_support_back(callback: CallbackQuery, state: FSMContext):
    if not callback.message:
        return
    await callback.message.edit_text(
        check_all_supports(check_support_messages()),
        reply_markup=ADMIN_SUPPORT_MESSAGES_MARKUPS(get_all_support_ids()),
        parse_mode="HTML",
    )