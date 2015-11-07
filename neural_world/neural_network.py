"""
Solving functions for neural network exploitation.

"""
from functools   import partial
from collections import deque
import pyasp.asp as asp
import os

import neural_world.config  as config
import neural_world.atoms   as atoms
import neural_world.commons as commons
from neural_world.commons import Direction


LOGGER = commons.logger()


def square_to_input_neurons(square):
    """From a set of objects, return states of associated input neurons

    square: set of objects (Nutrient, Individual).
    return: 2-tuple of boolean, that are the states of
            input neurons for given square.

    """
    empty = len(square) == 0
    if empty:
        contains_nutrients, contains_individuals = False, False
    else:
        contains_nutrients = any(o.is_nutrient for o in square)
        contains_individuals = any(o.is_individual for o in square)
    return contains_nutrients, contains_individuals


def react(individual, states:iter) -> tuple:
    """Return the individual's response to given input neuron states.

    individual: reference to an Individual instance.
    states: iterable of booleans, giving the state of input neurons.
    return: tuple of directions, result of reaction to environnment.

    """
    # Atoms creation:
    #  - define the neural network
    #  - add an atom up/1 or down/1 foreach input neuron according to its state
    input_atoms = individual.network_atoms + '.' + ''.join(
        ('up' if is_up else 'down') + '(' + str(neuron) + ').'
        # position in list gives the neuron id
        for neuron, is_up in enumerate(states)
    )
    LOGGER.debug('INPUT ATOMS: ' + input_atoms)
    # ASP solver call
    model = model_from(input_atoms, commons.ASP_SOLVING)
    LOGGER.debug('OUTPUT ATOMS: ' + str(model))
    # Directions of movement extraction: get id of up-state output neurons
    output_neurons_id = tuple(int(atoms.arg(a)) for a in model
                              if a.startswith('output_up('))
    # get the direction from the output neuron id:
    #  as output neurons are the last four with the biggest IDs,
    #  the maximal ID minus output neuron ID will give something
    #  between 0 and 3: that is directly convertable in Direction.
    return tuple(Direction.simplified(
        Direction(individual.max_neuron_id - ido)
        for ido in output_neurons_id
    ))


def clean(network_atoms):
    """Perform a cleaning on the neural network for remove useless neuron,
    give an orientation to edges,...

    network_atoms: string describing neural network through ASP atoms.
    output_neurons_ids: iterable of ids of output neurons.
    return: a new string describing neural network through ASP atoms, cleaned.

    """
    model = model_from(network_atoms, commons.ASP_CLEANING)
    LOGGER.warning('DEBUG commons.clean(1): ' + str(model.__class__) + str(model))
    LOGGER.warning('TODO commons.clean(1): test this function is necessary.')
    return '.'.join(model)


def model_from(base_atoms, aspfiles, aspargs={},
               gringo_options='', clasp_options=''):
    """Compute a model from ASP source code in aspfiles, with aspargs
    given as grounding arguments and base_atoms given as input atoms.

    base_atoms -- string, ASP-readable atoms
    aspfiles -- (list of) filename, contains the ASP source code
    aspargs -- dict of constant:value that will be set as constants in aspfiles
    gringo_options -- string of command-line options given to gringo
    clasp_options -- string of command-line options given to clasp

    """
    # use the right basename and use list of aspfiles in all cases
    if isinstance(aspfiles, str):
        aspfiles = [aspfiles]
    elif isinstance(aspfiles, tuple):  # solver take only list, not tuples
        aspfiles = list(aspfiles)

    # define the command line options for gringo and clasp
    constants = ' -c '.join(str(k)+'='+str(v) for k,v in aspargs.items())
    if len(aspargs) > 0:  # must begin by a -c for announce the first constant
        constants = '-c ' + constants
    gringo_options = ' '.join((constants, commons.ASP_GRINGO_OPTIONS, gringo_options))
    clasp_options += ' ' + ' '.join(commons.ASP_CLASP_OPTIONS)

    #  create solver and ground base and program in a single ground call.
    solver = asp.Gringo4Clasp(gringo_options=gringo_options,
                              clasp_options=clasp_options)
    # print('SOLVING:', aspfiles, constants)
    # print('INPUT:', base_atoms.__class__, base_atoms)
    answers = solver.run(aspfiles, additionalProgramText=base_atoms)
    # print('OK !')
    # print(len(answers), 'ANSWER(S):', '\n'.join(str(_) for _ in answers))

    # return the last solution (which is the best), or None if no solution
    try:
        last_solution = deque(answers, maxlen=1)[0]
        LOGGER.debug('SOLVING OUTPUT: ' + str(len(last_solution))
                     + ': ' + str(last_solution))
        return last_solution if len(last_solution) > 0 else None
    except IndexError:
        # no valid model
        return None
