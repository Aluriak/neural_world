"""Definition of generic solving routines,
encapsulating ASP calls through pyasp API.

"""
from pyasp import asp
from neural_world import commons


LOGGER = commons.logger(commons.SUBLOGGER_SOLVING)

# ASP SOLVING OPTIONS
ASP_GRINGO_OPTIONS = ''  # no default options
ASP_CLASP_OPTIONS  = ''  # options of solving heuristics
# ASP_CLASP_OPTIONS += ' -Wno-atom-undefined'
# ASP_CLASP_OPTIONS += ' --configuration=frumpy'
# ASP_CLASP_OPTIONS += ' --heuristic=Vsids'


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
    gringo_options = ' '.join((constants, ASP_GRINGO_OPTIONS, gringo_options))
    clasp_options += ' ' + ' '.join(ASP_CLASP_OPTIONS)

    #  create solver and ground base and program in a single ground call.
    solver = asp.Gringo4Clasp(gringo_options=gringo_options,
                              clasp_options=clasp_options)
    LOGGER.info('SOLVING: ' + str(aspfiles) + ' constants: ' + str(constants))
    answers = solver.run(aspfiles, additionalProgramText=base_atoms)

    # return the first found solution, or None if no solution
    try:
        assert len(answers) == 1
        first_solution = next(iter(answers))
        LOGGER.debug('SOLVING INPUT: ' + str(base_atoms))
        LOGGER.debug('SOLVING OUTPUT: ' + str(len(first_solution))
                     + ': ' + ' '.join(first_solution))
        return first_solution

    except StopIteration:
        # no valid model
        return None
