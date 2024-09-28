from aiogram import BaseMiddleware
from aiogram.types import Message
from database.users import get_user_by_id, add_user

class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if event.from_user:
            user = get_user_by_id(event.from_user.id)

            if not user:
                add_user(event)
        
        return await handler(event, data)
