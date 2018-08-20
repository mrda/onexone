
import datastore

debug = False


def person(command, arg=None):
    if debug:
        print("Entering person: command = {}, name = {}".
              format(command, arg))
    try:
        ds = datastore.get_datastore()
        if command == 'add':
            ds.new_entry(arg)
            ds.save()
        elif command == 'list':
            ds.list_entries()

    except Exception as e:
        print("Error in person: {}".format(e))
