"""
Definition of the concept of Neighbors.

"""
import itertools



def moore(coords):
    "Yields moore neighbors coords"
    x, y = coords
    return (
        (x+i, y+j)
        for i, j in itertools.product((-1, 0, 1), repeat=2)
        if i != 0 and j != 0
    )

def vonneumann(coords):
    return (
        (x+i, y+j)
        for i, j in (( 0, -1),
                     ( 1,  0),
                     ( 0,  1),
                     (-1,  0))
        if i != 0 and j != 0
    )
