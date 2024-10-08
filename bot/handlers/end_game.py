from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.FSM import GameState
from bot.markup import RESTART_MARKUP
from game.deck import calculate_result, add_cards
from config.language import RESTART
router = Router()

@router.message(GameState.END_GAME)
async def end_game(message: Message, state: FSMContext):
    data = await state.get_data()
    while data['dealer_score'] < 17 and data['user_score'] < 22 and data['user_score']>data['dealer_score']:
        data['dealer_cards'], data['dealer_score'] = add_cards(data['deck'], data['dealer_cards'], data['dealer_score'], 1)
    text = calculate_result(data['user_cards'], data['dealer_cards'], data['user_score'], data['dealer_score'], message.from_user.id)
    await state.clear()
    await message.answer(text, reply_markup=RESTART_MARKUP, parse_mode="HTML")