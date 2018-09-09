
import command
import datastore
import debugging

debug = False
debugging._debug = debug


class Person:

    def __init__(self):
        self.c = command.CommandOptions('person')
        self.c.add_command('list', self.list, "[all]")
        self.c.add_command('add', self.add, "<first> <last> [enabled]")
        self.c.add_command('delete', self.delete, "(<first> <last> | <nick>)")
        self.c.add_command('find', self.find, "<search-string>")
        self.c.add_command('info', self.info, "<search-string>")

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
    def find_person(self, person_str):
        # Note(mrda): Not used yet
        possible_persons = self._find([person_str])
        len_possible_persons = len(possible_persons)
        if len_possible_persons == 0:
            return (None, "No match found")
        elif len_possible_persons != 1:
            return (None, "No unique match found")
        else:
            return (True, possible_persons[0])

    @debugging.trace
    def _exact_match(self, first, last):

        first_result = self._search('first_name', first)
        if not first_result:
            return False

        last_result = self._search('last_name', last)
        if not last_result:
            return False

        intersection = [v for v in first_result if v in last_result]

        return len(intersection) == 1

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
            self.c.display_usage('add')
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
    def delete(self, args):
        len_args = len(args)
        if len_args < 1 or len_args > 2:
            self.c.display_usage('delete')
            return

        nick = None
        if len_args == 1:
            # Partial user supplied, go find a match
            nick = self._find(args)
            if len(nick) == 0:
                print("Couldn't find person '{}' to delete".format(args[0]))
                return
            elif len(nick) != 1:
                print("Multiple matches, won't delete {}".format(
                      " and ".join(nick)))
                return
        else:
            # Provided a first and last name, looking for an exact match
            first, last = args
            if self._exact_match(first, last):
                nick = self._build_nick((first, last))

        if raw_input("Are you sure you want to delete '{}'? ".
           format(nick[0])) not in ['Y', 'y']:
            print("Not deleting user")
            return

        ds = datastore.get_datastore()
        ds.remove_entry(nick[0])
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
