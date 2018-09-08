
import command
import datastore
import debugging

debug = False
debugging._debug = debug


class Person:

    @debugging.trace
    def __init__(self):
        self.c = command.CommandOptions('person')
        self.c.add_command('list', self.list, "[all]")
        self.c.add_command('add', self.add, "<first> <last> [enabled]")
        self.c.add_command('find', self.find, "<search-string>")
        self.c.add_command('info', self.info, "<search-string>")
        self.params = {}

    @debugging.trace
    def _is_match(self, candidate, wanted):
        # Exact match is easy
        if candidate == wanted:
            return True

        # Partial match occurs when the wanted string is a subset of
        # the candidate.  Note it needs to be the first part of the
        # candidate string.
        # Note(mrda): This could be improved
        candidate_len = len(candidate)
        wanted_len = len(wanted)
        if candidate_len > wanted_len:
            if wanted[0:wanted_len] == candidate[0:wanted_len]:
                return True

        return False

    @debugging.trace
    def _search(self, field, value):
        results = []
        try:
            ds = datastore.get_datastore()
            dictionary = ds.get_dict()
            for k, v in dictionary.iteritems():
                if self._is_match(v['meta'][field], value):
                    results.append(k)
            if results:
                return results
            return None
        except Exception as e:
            print("An exception got raised, {}".format(e))
            return None

    @debugging.trace
    def _find(self, args, interactive=False):
        results = []
        if len(args) != 1:
            print("Spurious arguments to `person find`")
        else:
            result = self._search('first_name', args[0])
            if result:
                for r in result:
                    results.append(r)
            result = self._search('last_name', args[0])
            if result:
                for r in result:
                    results.append(r)
            return results

    @debugging.trace
    def find(self, args):
        if len(args) != 1:
            self.c.display_usage('find')
            return

        results = self._find(args, True)
        if results:
            print("\n".join(results))
        else:
            print("No match found")

    @debugging.trace
    def info(self, args):
        if len(args) != 1:
            self.c.display_usage('info')
            return

        nick = self._find(args, False)
        if not nick:
            print("No record found")
            return
        for n in nick:
            self._print_person(n)
        print("")

    @debugging.trace
    def _print_person(self, nick):
        ds = datastore.get_datastore()
        dictionary = ds.get_value(nick)
        print("")
        print("First name: {}".format(dictionary['meta']['first_name']))
        print("Last name: {}".format(dictionary['meta']['last_name']))
        print("Enabled?: {}".format(dictionary['meta']['enabled']))
        print("One-on-One Meetings:")
        for entry in sorted(dictionary['meetings']):
            print("  {}".format(entry))

    @debugging.trace
    def _build_nick(self, args):
        nick = None if args[0] is None else args[0]
        if len(args) > 1:
            nick += args[1]
        return nick

    @debugging.trace
    def _new_person(self, first=None, last=None, enabled=True):
        p = {}
        p['meta'] = {}
        p['meta']['enabled'] = enabled
        p['meta']['first_name'] = first
        p['meta']['last_name'] = last
        p['meetings'] = ()
        return p

    @debugging.trace
    def add(self, args):
        len_args = len(args)
        if len_args < 2 or len_args > 3:
            print("Valid params for add are " + self.params['add'])
            return

        if len_args == 2:
            first, last = args
            enabled = True
        else:
            first, last, enabled = args

        ds = datastore.get_datastore()
        ds.new_entry(self._build_nick(args),
                     self._new_person(first, last, enabled))
        ds.save()

    @debugging.trace
    def list(self, args):
        len_args = len(args)

        ds = datastore.get_datastore()
        if len_args == 0:
            ds.list_keys()
        elif len_args == 1 and args[0] == 'all':
            ds.list_everything()
        else:
            self.c.display_usage('list')

    @debugging.trace
    def parse(self, args):
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in person.parse: {}".format(e))
