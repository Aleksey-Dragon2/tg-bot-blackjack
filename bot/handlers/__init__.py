from .user import game_start, start, move_player, end_game, stats, rating, rules, support, unknown_messages
from .admin import admin_start, offer_list, admin_list_user, inform_all, system_errors, relevant_offers, proccesing_offer, archive_offers

## unknown_messages.router - the latter, since it catches all messages that did not get into other handlers
routers = [
    start.router, game_start.router, move_player.router, end_game.router,
    stats.router, rating.router, rules.router, support.router, admin_start.router,
    offer_list.router, admin_list_user.router, inform_all.router, system_errors.router, 
    relevant_offers.router, proccesing_offer.router, archive_offers.router, unknown_messages.router
]