"""
Basical implementation of a terminal view for World object.

"""
import neural_world.commons as commons
import neural_world.actions as action
from neural_world.individual import Individual
from neural_world.nutrient import Nutrient
from . import observer


LOGGER = commons.logger()


class TerminalWorldView(observer.Observer, action.ActionEmitter):
    def __init__(self, engine):
        super().__init__(invoker=engine)
        self.graphics = {
            Nutrient: '·',
            Individual: '#',
        }


    def update(self, world, signals={}):
        """Print World in the terminal"""
        if len(signals) == 0 or observer.Signal.NEW_STEP in signals:
            print('\nstep:', world.step_number,
                  '\tindividuals:', world.object_counter[Individual])
            x_prev, line = 0, ''
            for coords, objects in world.ordered_objects:
                x, y = coords
                if x_prev != x:
                    x_prev = x
                    print('|', line, '|')
                    line = ''
                if len(objects) > 0:
                    if any(isinstance(o, Individual) for o in objects):
                        line += self.graphics[Individual]
                    else:
                        line += self.graphics[Nutrient]
                else:
                    line += ' '
