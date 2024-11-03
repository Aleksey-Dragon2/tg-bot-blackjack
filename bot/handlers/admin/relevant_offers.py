from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.language import ADMIN_SUPPORT_RELEVANT_LIST, ADMIN_MENU_SUPPORT, check_all_supports
from bot.markup import ADMIN_SUPPORT_MESSAGES_MARKUPS, ADMIN_SUPPORT_MENU_MARKUP

from database.supportsDB import get_all_support_ids, check_support_messages, check_support_message_by_id

from bot.env import SUPERUSERS
router = Router()

## Вывод списка актуальных предложений
@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_RELEVANT_LIST[0].casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_relevant_list(message: Message, state: FSMContext):
    await message.answer(
        check_all_supports(check_support_messages()),
        reply_markup=ADMIN_SUPPORT_MESSAGES_MARKUPS(get_all_support_ids()),
        parse_mode="HTML",
    )

## Вывод конкретного предложения
@router.callback_query(lambda c: any(c.data.startswith(f"help_{support_id}") for support_id in get_all_support_ids()))
async def admin_help_support(callback: CallbackQuery, state: FSMContext):
    support_id=callback.data.split("_")[1]
    if not callback.message:
        return
    await callback.message.edit_text(
        ADMIN_MENU_SUPPORT(check_support_message_by_id(support_id)),
        reply_markup=ADMIN_SUPPORT_MENU_MARKUP(support_id),
    )