"""
Definition of the Configuration class, that is a data holder.

"""
import neural_world.default as default
from neural_world.mutator import Mutator
from neural_world.commons import NeuronType
from neural_world.incubator import Incubator


class Configuration:
    """Contains data about a simulation.

    All data in configuration are one in:
        mutable: these values can change between two steps.
        unmutable: these values can't change without probable problems.

    Change data, even mutable, while running a step is probably a bad idea.

    Because of some postprocessing on the input values inside the
     configuration construction, its a bad idea to modify a field
     of an instance without call the postprocess_data() method after all changes.

    """
    MUTABLE_FIELDS = (
        'steps_number',  # number of steps to perform in one run
        'mutation_rate',
        'nutrient_regen',
        'nutrient_energy',
        'nutrient_density',
    )
    GENERATED_FIELDS = (
        'mutator', 'incubator'
    )

    def __init__(self, *,
                 # mutable fields
                 steps_number=1,
                 mutation_rate=default.MUTATION_RATE,
                 nutrient_regen=default.NUTRIENT_REGENERATION,
                 nutrient_energy=default.NUTRIENT_ENERGY,
                 nutrient_density=default.NUTRIENT_INITIAL_DENSITY,
                 # non mutable fields
                 space_width=default.SPACE_WIDTH,
                 space_height=default.SPACE_HEIGHT,
                 neighbor_access=default.NEIGHBOR_ACCESS,
                 neuron_output_type=default.OUTPUT_NEURON_TYPE,
                 neuron_output_count=default.OUTPUT_NEURON_COUNT,
                 life_division_min_energy=default.LIFE_DIVISION_MIN_ENERGY,
                 init_indiv_count=default.INDIVIDUAL_INITIAL_COUNT,
                 init_indiv_density=default.INDIVIDUAL_INITIAL_DENSITY,
                 neuron_inter_mincount=default.NEURON_INTER_MINCOUNT,
                 neuron_inter_maxcount=default.NEURON_INTER_MAXCOUNT,
                 neuron_edges_mincount=default.NEURON_EDGES_MINCOUNT,
                 neuron_edges_maxcount=default.NEURON_EDGES_MAXCOUNT
                ):
        for varname, value in locals().items():
            self.__dict__[varname] = value
        # add other data
        self.postprocess_data()
        self.terminated = False


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
            self.init_indiv_count is None or self.init_indiv_count >= 0,
            self.init_indiv_density is None or self.init_indiv_density >= 0,
            self.life_division_min_energy >= 0,
            isinstance(self.neuron_output_type, NeuronType),
            callable(self.neighbor_access),
        ))


    def postprocess_data(self):
        """Generate fields that needs it"""
        self.mutator   = Mutator(self)
        self.incubator = Incubator(self)
