"""
Definition of the Configurable abstract class

"""
from neural_world import commons
from functools import partial


LOGGER = commons.logger()


class Configurable:
    """A Configurable object provides API for manipulation of a
    Configuration object.

    Construction of the objects needs a Configuration object, and eventually
     the name of used fields in the configuration.
    The use_config() method allow to change configuration.

    If used fields are given to the constructor, fields will be added
     to the instance.
     When reference to config is changed, the fields keeped from the config
      are updated, according to the new config values.
      Moreover, all fields describing another Configurable instance will
       get there config field updated too.


    """

    def __init__(self, config, config_fields=[]):
        """Use the given config, and given fields.

        config: a Configuration instance.
        config_fields: iterable of config field (string)

        """
        self.__config_fields = config_fields
        self.config = config  # apply the field update

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, new_config):
        LOGGER.debug(str(self) + ' receive ' + repr(new_config))
        self.__config = new_config
        # update fields
        for field in self.__config_fields:
            setattr(self, field, getattr(new_config, field))
        # update linked Configurables
        for attr in self.__dict__.values():
            if isinstance(attr, Configurable):
                if attr.config is not new_config:  # change only if necessary
                    LOGGER.debug(str(self) + ' pass the config '
                                 + repr(new_config) + ' to ' + str(attr)
                                 + ' in place of ' + repr(attr.config))
                    attr.config = new_config
