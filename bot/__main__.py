"""entry point"""

import asyncio

from bot.client import dp, bot
from bot.handlers import routers
from bot.middlewares import UserCheckMiddleware
from database.usersDB import create_user_table
from database.supportsDB import create_support_table
from database.archive_supportDB import create_archive_support_table
create_user_table()
create_support_table()
create_archive_support_table()

for router in routers:
    dp.include_router(router)
dp.message.middleware.register(UserCheckMiddleware())

print("Start polling")
asyncio.run(dp.start_polling(bot))