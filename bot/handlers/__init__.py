from . import game_start, start, move_player, end_game, stats, rules, support, unknown_messages
from .admin import admin_start, offer_list, admin_list_user, inform_all
routers = [
    start.router, game_start.router, move_player.router, end_game.router,
    stats.router, rules.router, support.router, admin_start.router,
    offer_list.router, admin_list_user.router, inform_all.router, unknown_messages.router
]