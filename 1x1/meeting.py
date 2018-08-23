
import datastore
import person

debug = False


def _meeting_add(*args):
    if len(args) != 2:
        print("Wrong number of arguments to `meeting add`")
        return

    try:
        nickstr = args[0]
        datestr = args[1]

        ds = datastore.get_datastore()
        dictionary = ds.get_dict()

        # TODO(mrda): fixme.  We shouldn't be calling person here
        # We need code that handles the internal representation
        # of the 1x1 people and meetings
        nick = person._find(False, nickstr)
        dictionary[nick]['meetings'].append(datestr)

        ds.save()
    except Exception as e:
        print("An exception got raised, {}".format(e))


def meeting(*args):
    if debug:
        print("Entering meeting: args={}".format(*args))
    command = args[0]
    remaining = args[1:]
    try:
        ds = datastore.get_datastore()
        if command == 'add':
            _meeting_add(*remaining)

        # elif command == 'delete':
        #    None
        # elif command == 'latest':
        #    # Show the latest meetings for all staff
        #    None
        # elif command == 'help':
        #    None
        else:
            # TODO(mrda): Help
            None

    except Exception as e:
        print("Error in meeting: {}".format(e))
