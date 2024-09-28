from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.database import get_user_by_id, add_user, create_user_table, create_support_table

class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        create_user_table()
        create_support_table()
        if event.from_user:
            user = get_user_by_id(event.from_user.id)

            if not user:
                add_user(event)
        
        return await handler(event, data)
