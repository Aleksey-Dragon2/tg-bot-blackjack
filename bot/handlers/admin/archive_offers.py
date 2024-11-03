from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.language import ADMIN_SUPPORT_ARCHIVE_LIST, check_all_supports_archive
from config.language import ADMIN_PANEL, ADMIN_SUPPORT_MENU_BACK
from bot.markup import ADMIN_MARKUP

from database.archive_supportDB import check_archive_support_messages

from bot.env import SUPERUSERS
router = Router()



## Вывод списка предложений в архиве
@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_ARCHIVE_LIST[0].casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_archive_list(message: Message, state: FSMContext):
    await message.answer(
        check_all_supports_archive(check_archive_support_messages()),
        parse_mode="HTML",
    )

## Возвращение назад к выборы списка предложений
@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_MENU_BACK[0].casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_menu_back(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_PANEL,
        reply_markup=ADMIN_MARKUP,
    )