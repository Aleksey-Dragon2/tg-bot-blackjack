from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config.language import ADMIN_SUPPORT_LIST
from config.language import  ADMIN_CHOISE_SUPPORT_LIST
from bot.markup import ADMIN_SUPPORT_LIST_MARKUP

from bot.env import SUPERUSERS
router = Router()

## Выыбор списка предложений
@router.message(lambda message: message.text.casefold()==ADMIN_SUPPORT_LIST.casefold() and message.from_user.id in [int(user) for user in SUPERUSERS])
async def admin_support_list(message: Message, state: FSMContext):
    await message.answer(
        ADMIN_CHOISE_SUPPORT_LIST,
        reply_markup=ADMIN_SUPPORT_LIST_MARKUP
    )