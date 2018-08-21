
class CommandOptions:

    def __init__(self, debug=False):
        self.commands = {}
        self.debug = debug

    def add_command(self, command, func):
        if self.debug:
            print("Registering '{}' to {}".format(command, func))
        self.commands[command] = func
        if self.debug:
            self.show_jumptable()
            print("\n")

    def get_commands(self):
        return sorted(self.commands.keys())

    def jump(self, *args):
        command = args[0]
        rest = args[1:]
        if self.debug:
            print("jump: About to invoke '{}' with args '{}'".
                  format(command, rest))
        try:
            func = self.commands[command]
            func(*rest)
        except KeyError as e:
            print("Unknown subcommand: {}".format(", ".join(args)))
            self.usage()
        except Exception as e:
            print("Problem invoking subcommand '{}' ({})".format(command, e))

    def show_jumptable(self):
        print("==== Jump table ====")
        print self.commands

    def usage(self):
        print("Valid commands are:")
        print("\n".join(self.get_commands()))
