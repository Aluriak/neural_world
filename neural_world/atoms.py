"""
Primitives for easier manipulation of atoms outputting by ASP solving.

"""
from collections        import namedtuple


# Atom definition
ATOM = namedtuple('Atom', ['name', 'args'])


def split(atom):
    """Return the splitted version of given atom.

    atom -- string formatted as an ASP readable atom

    >>>> split('edge(lacA,lacZ)')
    ('edge', ('lacA', 'lacZ'))

    """
    payload = atom.strip('.').strip(')')
    try:
        pred, data = payload.split('(')
        return ATOM(pred, tuple(data.split(',')))
    except ValueError:  # no args !
        return ATOM(payload, None)


def arg(atom):
    """Return the argument of given atom, as a tuple if necessary.

    If the atom have only one arg, the arg itself will be used.

    >>>> split('edge(lacA,lacZ)')
    ('lacA', 'lacZ')
    >>>> split('score(13)')
    '13'
    >>>> split('lowerbound')
    None

    """
    payload = atom.strip('.').strip(')')
    try:
        data = tuple(payload.split('(')[1].split(','))
        if len(data) > 1:
            return data
        else:
            return next(iter(data))
    except ValueError:  # no args !
        return None
