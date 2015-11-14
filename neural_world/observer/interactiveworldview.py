"""
Implementation of a terminal view for World object,
that offer a prompt for create commands for the engine.

"""
import time
import sys

from functools import partial
from threading import Thread

from prompt_toolkit import prompt

import neural_world.commons as commons
from neural_world.actions import QuitAction
from neural_world.individual import Individual
from neural_world.nutrient import Nutrient
from . import terminalworldview as worldview


LOGGER = commons.logger()
PROMPT_WELCOME = '?> '


class InteractiveTerminalWorldView(worldview.TerminalWorldView):
    def __init__(self, engine):
        super().__init__(engine)
        self.get_input = partial(prompt, PROMPT_WELCOME, patch_stdout=True)
        Thread(target=self.run).start()
        time.sleep(0.1)

    def run(self):
        """do the prompt job"""
        try:
            while True:
                print(self.get_input())
        except (KeyboardInterrupt, EOFError):
            pass
        self.quit()

    def quit(self):
        """Send a quit command to the engine"""
        self.engine.add(QuitAction())


