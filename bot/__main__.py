"""entry point"""

import asyncio

from bot.client import dp, bot
from bot.handlers import routers
from bot.middlewares import UserCheckMiddleware

for router in routers:
    dp.include_router(router)
dp.message.middleware.register(UserCheckMiddleware())
print("Start polling")
asyncio.run(dp.start_polling(bot))