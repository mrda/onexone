
import command
import datastore
import debugging
import person

debug = False
debugging._debug = debug


class Meeting:

    def __init__(self):
        self.c = command.CommandOptions('meeting')
        self.c.add_command('add', self.add, "<person> <date>")
        self.p = person.Person()

    @debugging.trace
    def add(self, args):
        len_args = len(args)
        if len_args != 2:
            self.c.display_usage('add')
            return

        name = args[0]
        meeting = args[1]
        matches = self.p._find([name], False)
        if not matches:
            print("Can't find '{}'".format(name))
            return
        if len(matches) > 1:
            print("Multiple persons found: {}".format(matches))
            return
        # Note(mrda): Shouldn't be playing with the internals of
        # entries here.  We need code to abstract this
        ds = datastore.get_datastore()
        dictionary = ds.get_dict()
        dictionary[matches[0]]['meetings'].append(meeting)
        ds.save()

    @debugging.trace
    def parse(self, args):
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in meeting.parse: {}".format(e))
