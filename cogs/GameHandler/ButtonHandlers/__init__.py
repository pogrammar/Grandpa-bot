from typing import NamedTuple

from .aki import Akinator
from .ConnectFour import ConnectFour
from .rps import RockPaperScissors
from .ButtonHandlers import *

__all__ = (
    'Akinator', 
    'ConnectFour',
    'RockPaperScissors',
    "BetaAkinator",
    "MemoryGame",
    "BetaRockPaperScissors",
)