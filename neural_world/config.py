"""
Definition of the Configuration class, that is a data holder.

"""
from functools import partial
from collections import namedtuple
from collections import ChainMap

import neural_world.default as default
import neural_world.commons as commons
from neural_world.mutator import Mutator
from neural_world.commons import NeuronType
from neural_world.incubator import Incubator


# Definition of a Configuration Field payload:
#  a field have a value and an associated type
#  here the type is function that can turn a string into a particular type.
#  (ex: int, float, str, Direction,…)
Field = namedtuple('Field', ['value', 'type'])
# Free type: when the considered object doesn't have a particular type
def free_type(x): return x
# Better boolean management
def user_compliant_bool(x):
    try:
        return bool(int(x))
    except ValueError:
        return 't' in x.lower()


class Configuration:
    """Contains data about a simulation.

    All data in configuration are one in:
        mutable: these values can change between two steps.
        unmutable: these values can't change without probable problems.
        generated: these values are deduced from the rest of the data.

    Change data, even mutable, while running a step is probably a bad idea.

    Because of the generated data, its a bad idea to modify a field
     of a Configuration instance without call the postprocess_data()
     method after all changes.
     This method will generate the generated data.

    """

    MUTABLE_FIELDS = {
        'steps_number'     : Field(value=default.STEP_NUMBER_PER_RUN, type=int),
        'mutation_rate'    : Field(value=default.MUTATION_RATE, type=float),
        'nutrient_regen'   : Field(value=default.NUTRIENT_REGENERATION, type=float),
        'nutrient_energy'  : Field(value=default.NUTRIENT_ENERGY, type=int),
        'nutrient_density' : Field(value=default.NUTRIENT_INITIAL_DENSITY, type=float),
        'waiting_time'     : Field(value=default.WAITING_TIME, type=float),
        'terminated'       : Field(value=False, type=user_compliant_bool),
    }
    GENERATED_FIELDS = {
        'mutator'   : Field(value=None, type=free_type),
        'incubator' : Field(value=None, type=free_type),
    }
    UNMUTABLE_FIELDS = {
        'space_width'              : Field(value=default.SPACE_WIDTH, type=int),
        'space_height'             : Field(value=default.SPACE_HEIGHT, type=int),
        'neighbor_access'          : Field(value=default.NEIGHBOR_ACCESS, type=free_type),
        'neuron_output_type'       : Field(value=default.OUTPUT_NEURON_TYPE, type=free_type),
        'neuron_output_count'      : Field(value=default.OUTPUT_NEURON_COUNT, type=int),
        'life_division_min_energy' : Field(value=default.LIFE_DIVISION_MIN_ENERGY, type=int),
        'init_indiv_count'         : Field(value=default.INDIVIDUAL_INITIAL_COUNT, type=int),
        'init_indiv_density'       : Field(value=default.INDIVIDUAL_INITIAL_DENSITY, type=float),
        'neuron_inter_mincount'    : Field(value=default.NEURON_INTER_MINCOUNT, type=int),
        'neuron_inter_maxcount'    : Field(value=default.NEURON_INTER_MAXCOUNT, type=int),
        'neuron_edges_mincount'    : Field(value=default.NEURON_EDGES_MINCOUNT, type=int),
        'neuron_edges_maxcount'    : Field(value=default.NEURON_EDGES_MAXCOUNT, type=int),
        'dir_archive_simulation'   : Field(value=default.DIR_SIMULATION_ARCHIVE, type=str),
    }
    ALL_FIELDS = ChainMap({}, MUTABLE_FIELDS, UNMUTABLE_FIELDS, GENERATED_FIELDS)

    def __init__(self, **kwargs):
        # get dict fieldname:Field received as parameter
        parameters = {
            field: Field(value=Configuration.typed(field, value),
                         type=Configuration.ALL_FIELDS[field].type)
            for field, value in kwargs.items()
        }
        # take parameters in priority, else the ALL_FIELDS dict
        prioritized_fields = ChainMap(parameters, Configuration.ALL_FIELDS)
        # save values as fields
        for varname, field in prioritized_fields.items():
            value, ftype = field
            setattr(self, '_' + varname, ftype(value))
        # access and setter definition
        def field_access(instance, field):
            return getattr(instance, '_' + field)
        def field_setter(instance, value, field):
            ftype = Configuration.ALL_FIELDS[field].type
            setattr(instance, '_' + field, ftype(value))
            # regenerate generated data
        # add values as properties, eventually with a setter if field is mutable
        for varname in Configuration.ALL_FIELDS:
            new_prop = property(partial(field_access, field=varname))
            setattr(Configuration, varname, new_prop)
            if varname in Configuration.MUTABLE_FIELDS:
                setter = new_prop.setter(partial(field_setter, field=varname))
                setattr(Configuration, varname, setter)
        # add other data
        self.postprocess_data()

    @classmethod
    def typed(cls, varname, value):
        try:
            # get a Field namedtuple, and use the type for convert the value
            return cls.ALL_FIELDS[varname].type(value)
        except KeyError:
            LOGGER.error("Configuration.__init__ receive an invalid field name:"
                         + '"' + varname + '".')
            return value

    def is_valid(self):
        """Return True if self data is valid"""
        return all((
            # mutable fields
            type(self.terminated) is bool,
            self.steps_number > 0,
            self.mutation_rate >= 0.,
            self.nutrient_energy  >= 0,
            self.nutrient_density >= 0.,
            self.nutrient_regen   >= 0.,
            # non mutable fields
            self.space_width  > 0,
            self.space_height > 0,
            self.nutrient_energy >= 0,
            self.neuron_output_count > 0,
            isinstance(self.init_indiv_count, int),
            isinstance(self.init_indiv_density, float),
            self.life_division_min_energy >= 0,
            isinstance(self.neuron_output_type, NeuronType),
            callable(self.neighbor_access),
        ))


    def postprocess_data(self):
        """Generate fields that needs it"""
        self._mutator   = Mutator(self)
        self._incubator = Incubator(self)

    def __str__(self):
        ITEM_SEP = '\n\t'
        mutable_fields   = sorted(f for f in Configuration.MUTABLE_FIELDS)
        mutable_maxlen   = len(max(mutable_fields, key=len))
        unmutable_fields = sorted(f for f in Configuration.UNMUTABLE_FIELDS)
        unmutable_maxlen = len(max(unmutable_fields, key=len))
        printed_fields = sorted(self.all_fields)
        # string construction
        return 'Configuration (mutable)' + ITEM_SEP + ITEM_SEP.join(
            fname.ljust(mutable_maxlen) + ' : ' + str(getattr(self, fname))
            for fname in mutable_fields
        ) + '\n\nConfiguration (unmutable)' + ITEM_SEP + ITEM_SEP.join(
            fname.ljust(unmutable_maxlen) + ' : ' + str(getattr(self, fname))
            for fname in unmutable_fields
        )

    @property
    def all_fields(self):
        return (k for k in Configuration.ALL_FIELDS.keys())

    @property
    def mutable_fields(self):
        return (k for k in Configuration.MUTABLE_FIELDS.keys())
