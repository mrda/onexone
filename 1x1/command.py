import sys


class CommandOptions:

    def __init__(self, debug=False):
        self.commands = {}
        self.commands['default'] = self.default_option
        self.debug = debug

    def add_command(self, command, func):
        if self.debug:
            print("Registering '{}' to {}".format(command, func))
        self.commands[command] = func
        if self.debug:
            self.show_jumptable()
            print("\n")

    def default_option(self):
        print("Unknown command: '{}' with args '{}'".format(sys.argv[1],
                                                            sys.argv[2:]))

    def jump(self, *args):
        command = args[0]
        rest = args[1:]
        if self.debug:
            print("jump: About to invoke '{}' with args '{}'".
                  format(command, rest))
        try:
            self.commands[command](*rest)
        except Exception as e:
            print(e)
            self.commands['default']()

    def show_jumptable(self):
        print("==== Jump table ====")
        print self.commands
