from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.language import ADMIN_SUPPORT_LIST, ADMIN_SUPPORT_RELEVANT_LIST, ADMIN_SUPPORT_ARCHIVE_LIST, check_all_supports, ADMIN_MENU_SUPPORT, ADMIN_SUPPORT_MENU_BACK
from config.language import ADMIN_PANEL, ADMIN_CHOISE_SUPPORT_LIST, ADMIN_MESSAGE_PROCESSED
from bot.markup import ADMIN_SUPPORT_MESSAGES_MARKUPS, ADMIN_SUPPORT_MENU_MARKUP, ADMIN_SUPPORT_LIST_MARKUP, ADMIN_MARKUP

from database.supportsDB import get_all_support_ids, check_support_messages, check_support_message_by_id
from database.archive_supportDB import move_support_to_archive, check_archive_support_messages

from bot.env import SUPERUSERS
router = Router()

@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_LIST.casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_list(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_CHOISE_SUPPORT_LIST,
        reply_markup=ADMIN_SUPPORT_LIST_MARKUP
    )

@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_RELEVANT_LIST[0].casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_relevant_list(message: Message, state: FSMContext):
    await message.answer(
        check_all_supports(check_support_messages()),
        reply_markup=ADMIN_SUPPORT_MESSAGES_MARKUPS(get_all_support_ids()),
        parse_mode="HTML",
    )

@router.callback_query(lambda c: any(c.data.startswith(f"help_{support_id}") for support_id in get_all_support_ids()))
async def admin_help_support(callback: CallbackQuery, state: FSMContext):
    support_id=callback.data.split("_")[1]
    if not callback.message:
        return
    await callback.message.edit_text(
        ADMIN_MENU_SUPPORT(check_support_message_by_id(support_id)),
        reply_markup=ADMIN_SUPPORT_MENU_MARKUP(support_id),
    )

@router.callback_query(lambda c: c.data.startswith("admin_support_confirm_"))
async def admin_support_confirm(callback: CallbackQuery, state: FSMContext):
    support_id=callback.data.split("_")[3]
    move_support_to_archive(support_id, 'Accepted')
    if not callback.message:
        return
    await callback.message.edit_text(
        ADMIN_MESSAGE_PROCESSED
    )

@router.callback_query(lambda c: c.data.startswith("admin_support_deny_"))
async def admin_support_deny(callback: CallbackQuery, state: FSMContext):
    support_id=callback.data.split("_")[3]
    move_support_to_archive(support_id, 'Denied')
    if not callback.message:
        return
    await callback.message.edit_text(
        ADMIN_MESSAGE_PROCESSED
    )

@router.callback_query(lambda c: c.data.startswith("admin_support_back_"))
async def admin_support_back(callback: CallbackQuery, state: FSMContext):
    if not callback.message:
        return
    await callback.message.delete()

@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_ARCHIVE_LIST[0].casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_archive_list(message: Message, state: FSMContext):
    await message.answer(
        check_all_supports(check_archive_support_messages()),
        parse_mode="HTML",
    )

@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_MENU_BACK[0].casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_menu_back(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_PANEL,
        reply_markup=ADMIN_MARKUP,
    )