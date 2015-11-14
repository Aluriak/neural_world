"""
Definition of the Prompt class, designed for editing Configuration
 with a terminal prompt.

"""
from functools import partial

from prompt_toolkit import prompt

import neural_world.commons as commons


LOGGER = commons.logger()
PROMPT_WELCOME = '?> '


class Prompt:

    def __init__(self):
        self._get_input = partial(prompt, PROMPT_WELCOME)

    def input(self):
        self._handle(self._get_input())

    def _handle(self, command):
        pass
