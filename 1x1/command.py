import debugging
import utils


class CommandOptions:

    def __init__(self, subcommand=None, debug=False):
        self.commands = {}
        self.subcommand = subcommand
        self.debug = debug

    @debugging.trace
    def add_command(self, command, func, valid_args=None):
        if self.debug:
            print("Registering '{}' to {}".format(command, func))
        self.commands[command] = (func, valid_args)
        if self.debug:
            self.show_jumptable()
            print("\n")

    def get_commands(self):
        return sorted(self.commands.keys())

    @debugging.trace
    def jump(self, args):
        command = args[0]
        rest = args[1:]
        if self.debug:
            print("jump: About to invoke '{}' with args '{}'".
                  format(command, rest))
        try:
            func = self.commands[command][0]
            func(rest)
        except KeyError as e:
            print("Unknown subcommand: {}".format(", ".join(args)))
            self.usage()
        except Exception as e:
            print("Problem invoking subcommand '{}' ({})".format(command, e))

    def show_jumptable(self):
        print("==== Jump table ====")
        print self.commands

    def display_usage(self, command):
        if command not in self.commands:
            print("*** No such subcommand defined")
            return
        print("Usage: {} {}".format(command, self.commands[command][1]))

    def usage(self, args=None):
        # Note(mrda): Deliberately ignoring args
        utils.display_program_header()
        if self.subcommand:
            print("Valid subcommands for '{}' are:".format(self.subcommand))
        else:
            print("Valid commands are:")
        for command in sorted(self.commands.keys()):
            print("  {} {}".format(command, self.commands[command][1]))
