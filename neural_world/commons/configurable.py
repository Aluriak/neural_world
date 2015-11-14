"""
Definition of the Configurable abstract class

"""
from functools import partial


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
        self.__config = new_config
        # update fields
        for field in self.__config_fields:
            self.__dict__[field] = new_config.__dict__[field]
        # update linked Configurables
        for field, value in self.__dict__.items():
            if isinstance(value, Configurable):
                if value.config is not new_config:  # change only if necessary
                    self.__dict__[field].config = new_config


if __name__ == '__main__':
    class ConfigMock:
        def __init__(self, a=42):
            self.a = a
            self.b = 'hello, world'
            self.c = False

    config = ConfigMock()
    m1 = Configurable(config, config_fields=['a', 'b'])
    assert config.a == m1.a
    assert config.b == m1.b
    assert not hasattr(m1, 'c')

    m2 = Configurable(config, config_fields=['b', 'c'])
    m2.other_m = m1  # m2 know m1
    assert not hasattr(m2, 'a')
    assert config.b == m2.b
    assert config.c == m2.c

    # update config: field 'a' have changed
    new_config = ConfigMock(a='is propagation working ?')
    m2.config = new_config  # change configuration of m2 (so of m1, too)
    assert new_config.a == m1.a  # m1 change for the new config
    assert not hasattr(m2, 'a')  # m2 doesn't care about the changed field
