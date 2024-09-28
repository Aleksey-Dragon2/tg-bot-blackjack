from aiogram import Router
from aiogram.types import Message
from bot.FSM import GameState
from aiogram.fsm.context import FSMContext
from bot.markup import GAME_MARKUP
from game.deck import add_cards
from config.language import GAME_INFO, GET_CARD, STOP, GAME_INVALID_MOVE
from bot.handlers.end_game import end_game

router = Router()

@router.message(GameState.PLAYER_TURN)
async def player_turn(message: Message, state: FSMContext):
    text = await GAME_INFO(message, state)
    await message.answer(text, reply_markup=GAME_MARKUP, parse_mode="HTML")
    await state.set_state(GameState.WAITING_FOR_PLAYER_ACTION)


@router.message(lambda message: message.text.casefold() in [cmd.casefold() for cmd in GET_CARD])
async def handle_get_card(message: Message, state: FSMContext):
    data = await state.get_data()
    data['user_cards'], data['user_score'] = add_cards(data['deck'], data['user_cards'], data['user_score'], 1)
    await state.update_data(
        user_cards=data['user_cards'],
        user_score=data['user_score'],
        dealer_cards=data['dealer_cards'],
        dealer_score=data['dealer_score']
    )
    
    if data['user_score'] >= 21:
        await state.set_state(GameState.END_GAME)
        await end_game(message, state)
    else:
        await player_turn(message, state)

@router.message(GameState.WAITING_FOR_PLAYER_ACTION, lambda message: message.text.casefold() in [cmd.casefold() for cmd in STOP])
async def handle_stop(message: Message, state: FSMContext):
    await state.set_state(GameState.END_GAME)
    await end_game(message, state)

@router.message(GameState.WAITING_FOR_PLAYER_ACTION)
async def handle_invalid_action(message: Message, state: FSMContext):
    await message.answer(GAME_INVALID_MOVE)
    await player_turn(message, state)