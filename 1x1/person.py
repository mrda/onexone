
import datastore

debug = False


def _new_person(first=None, last=None, enabled=True):
    p = {}
    p['meta'] = {}
    p['meta']['enabled'] = enabled
    p['meta']['first_name'] = first
    p['meta']['last_name'] = last
    p['meetings'] = ()
    return p


def _print_person(nick):
    ds = datastore.get_datastore()
    dictionary = ds.get_value(nick)
    print("First name: {}".format(dictionary['meta']['first_name']))
    print("Last name: {}".format(dictionary['meta']['last_name']))
    print("Enabled?: {}".format(dictionary['meta']['enabled']))
    print("One-on-One Meetings:")
    for entry in sorted(dictionary['meetings']):
        print("  {}".format(entry))


def _build_nick(*args):
    nick = None
    nick = None if args[0] is None else args[0]
    if len(args) > 1:
        nick += args[1]
    return nick


def _list(*args):
    if args:
        print("Spurious arguments to `person list`")
    else:
        ds = datastore.get_datastore()
        ds.list_keys()


def _is_match(candidate, wanted):
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


def _search(field, value):
    try:
        ds = datastore.get_datastore()
        dictionary = ds.get_dict()
        for k, v in dictionary.iteritems():
            if _is_match(v['meta'][field], value):
                return k
        return None
    except Exception as e:
        print("An exception got raised, {}".format(e))
        return None


def _find(interactive, *args):
    if len(args) != 1:
        print("Spurious arguments to `person find`")
    else:
        result = _search('first_name', args[0])
        if not result:
            result = _search('last_name', args[0])

        if not interactive:
            return result

        if result:
            print(result)
        else:
            print("No match found")


def _info(*args):
    nick = _find(False, *args)
    if not nick:
        print("No record found")
        return
    _print_person(nick)


def person(*args):
    if debug:
        print("Entering person: args={}".format(*args))
    command = args[0]
    remaining = args[1:]
    try:
        ds = datastore.get_datastore()
        if command == 'add':
            ds.new_entry(_build_nick(*remaining), _new_person(*remaining))
            ds.save()
        elif command == 'list':
            _list(*remaining)
        elif command == 'find':
            _find(True, *remaining)
        elif command == 'info':
            _info(*remaining)
        else:
            # TODO(mrda): Help
            None

    except Exception as e:
        print("Error in person: {}".format(e))
