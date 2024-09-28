from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class GameState(StatesGroup):
    PLAYER_TURN = State()
    WAITING_FOR_PLAYER_ACTION = State()
    END_GAME = State()
    CHOOSING_SUPPORT = State()
    SUPPORT_MESSAGE = State()
    CONFIRM_SUPPORT_MESSAGE = State()

class AdminState(StatesGroup):
    SENDING_MESSAGE_ALL = State()
    AWAITING_CONFIRMATION = State()