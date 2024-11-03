import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config.language import START_GAME, RESTART
from bot.FSM import GameState
from game.deck import get_deck, add_cards
from bot.handlers.user.move_player import player_turn
router = Router()


@router.message(Command('start_game'))
@router.message(F.text.casefold().in_([START_GAME.casefold(), RESTART.casefold()]))
async def game_start(message: Message, state: FSMContext):
    deck=get_deck()
    user_cards, user_score=add_cards(deck,[],0,2)
    dealer_cards, dealer_score=add_cards(deck,[],0,2)
    await state.update_data(
    deck=deck,
    user_cards=user_cards,
    dealer_cards=dealer_cards,
    user_score=user_score,
    dealer_score=dealer_score
    )

    if user_score>=21:
        await state.set_state(GameState.END_GAME)
    else:
        await state.set_state(GameState.PLAYER_TURN)
        await player_turn(message, state)