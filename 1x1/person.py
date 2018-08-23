
import datastore

debug = False


def _new_person(nick, first=None, last=None, enabled=True):
    p = {}
    p['meta'] = {}
    p['meta']['enabled'] = enabled
    p['meta']['first_name'] = first
    p['meta']['last_name'] = last
    p['meetings'] = ()
    return p


def person(command, arg=None):
    if debug:
        print("Entering person: command = {}, name = {}".
              format(command, arg))
    try:
        ds = datastore.get_datastore()
        if command == 'add':
            ds.new_entry(arg, _new_person(arg))
            ds.save()
        elif command == 'list':
            ds.list_entries()

    except Exception as e:
        print("Error in person: {}".format(e))
