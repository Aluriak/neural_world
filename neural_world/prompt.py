"""
Definition of the Prompt class, designed for editing Configuration
 with a terminal prompt.

"""
from functools import partial

from prompt_toolkit import prompt
from prompt_toolkit.contrib.regular_languages.compiler   import compile as pt_compile
from prompt_toolkit.contrib.completers                   import WordCompleter
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter

import neural_world.commons as commons
import neural_world.actions as actions


LOGGER = commons.logger()
PROMPT_WELCOME = '?> '

COMMAND_NAMES = {
    # command id: command aliases
    'quit': ('quit', 'exit', ':q', 'q'),
    'help': ('help', 'wtf', ':h', 'h'),
    'conf': ('config', 'conf', ':c', 'c', ':p', 'p'),
    'set' : ('set', ':s', 's'),
    'get' : ('get', ':g', 'g'),
    'apply': ('apply', ':a', 'a'),
}


def commands_grammar(config, commands=COMMAND_NAMES):
    """Return a grammar for given commands (dict command:aliases)
    that use given Configuration for field autocompletion.

    """
    def aliases(cmd):
        """access the aliases of given (sub)command.
        if not in commands dict, will use it as an iterable."""
        try:             return '|'.join(commands[cmd])
        except KeyError: return '|'.join(cmd)
    def cmd2reg(cmd, subcmd=None, args=None):
        """layout automatization"""
        return (
            '(\s*  (?P<cmd>(' + aliases(cmd) + '))'
            + ('' if subcmd is None
               else ('\s+  (?P<subcmd>('+ aliases(subcmd) + '))   \s*  '))
            + ('' if args   is None else  ('\s+  (?P<args>(.*))   \s*  '))
            + ') |\n'
        )
    # get grammar, log it and return it
    grammar = (
          cmd2reg('quit', None, None)
        + cmd2reg('help', None, None)
        + cmd2reg('conf', None, None)
        + cmd2reg('set', config.mutable_fields, True)
        + cmd2reg('get', config.all_fields, None)
        + cmd2reg('apply', None, None)
    )
    LOGGER.debug('PROMPT GRAMMAR:\n' + str(grammar))
    return pt_compile(grammar)


class Prompt(actions.ActionEmitter):

    def __init__(self, config, invoker):
        super().__init__(invoker)
        self.config = config
        self.grammar = commands_grammar(config)
        completer = GrammarCompleter(
            self.grammar,
            {'subcmd': WordCompleter(tuple(config.all_fields))}
        )
        self._get_input = partial(prompt, PROMPT_WELCOME, completer=completer)

    def input(self):
        """Handle user input, until user want to apply the config"""
        while not self._handle(self._get_input()): pass

    def _handle(self, input_text):
        """Return True when the user asks for leave the prompt"""
        match = self.grammar.match(input_text)
        if match is None:
            print('invalid command')
            return False  # do not quit the prompt
        elif len(input_text) == 0:
            return False
        else:
            values = match.variables()
            subcmd = values.get('subcmd')
            args = values.get('args')
            cmd = next(  # get root name, not an alias
                cmd_name
                for cmd_name, aliases in COMMAND_NAMES.items()
                if values.get('cmd') in aliases
            )
            # call function associated with the command
            leave_prompt = bool(getattr(self, 'on_' + cmd)(subcmd, args))
            return leave_prompt
        return False

    def on_quit(self, subcmd:None=None, args:None=None):
        """send a quit request to the simulation, and leave the prompt"""
        self.invoker.add(actions.QuitAction())
        return True  # leave the prompt

    def on_apply(self, subcmd:None=None, args:None=None):
        """Leave the prompt, then apply the configuration to the simulation"""
        return True  # leave the prompt

    def on_conf(self, subcmd:None=None, args:None=None):
        """show the config"""
        print(self.config)

    def on_set(self, config_field, args):
        """set given value for given mutable config field
        ex: set mutation_rate 0.2"""
        setattr(self.config, config_field, args)
        print(config_field, 'set to', getattr(self.config, config_field))

    def on_get(self, config_field, args:None=None):
        """show value of given config field
        ex: get space_height"""
        print(config_field + ':', getattr(self.config, config_field))

    def on_help(self, subcmd:None=None, args:None=None):
        """show this help"""
        callbacks = tuple(sorted(
            attrname[3:] for attrname in self.__dir__()
            if attrname.startswith('on_')
        ))
        maxlen = len(max(callbacks, key=len))
        # printings !
        for callback in callbacks:
            print(callback.rjust(maxlen) + ':',
                  getattr(self, 'on_' + callback).__doc__)
