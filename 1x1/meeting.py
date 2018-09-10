
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
        self.c.add_command('up-next', self.up_next, "")
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
    def get_latest_meeting(self, nick):
        """ Given a nick find the last 1x1 meeting they had"""
        ds = datastore.get_datastore()

        mtgs = ds.get_meetings(nick)
        if not mtgs:
            return None

        meetings = sorted(mtgs, reverse=True)
        return meetings[0]

    @debugging.trace
    def up_next(self, args):
        """ Find the next people who are up next for a 1x1 """
        # Note(mrda): Ignoring args

        # Get the latest meeting slot for each person who is enabled
        ds = datastore.get_datastore()
        last_meeting = {}
        for nick in ds.ds.keys():
            if not self.p.is_enabled(nick):
                continue
            mtg = self.get_latest_meeting(nick)
            if not mtg:
                mtg = 0

            last_meeting[nick] = mtg

        # Sort list in reverse chronological order
        people_meetings = sorted(last_meeting.iteritems(),
                                 key=lambda (k, v): (v, k))

        # Display
        format_str = "{:>{}}  {:>8}"
        max_name_len = 0

        # Find longest name first
        for pm in people_meetings:
            if len(pm[0]) > max_name_len:
                max_name_len = len(pm[0])

        print(format_str.format("Name", max_name_len, "Last 1x1"))
        print(format_str.format("----", max_name_len, "--------"))
        for pm in people_meetings:
            # TODO(mrda): Resolve why this needs to be compared to True
            if self.p.is_enabled(pm[0]) == True:
                meeting = "never"
                if pm[1] != 0:
                    meeting = pm[1]
                print(format_str.format(pm[0], max_name_len, meeting))

    @debugging.trace
    def parse(self, args):
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in meeting.parse: {}".format(e))
