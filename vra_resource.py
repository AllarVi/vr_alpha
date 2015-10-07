__author__ = 'Mart'

from vra_io import load_hosts


def resource_handler(sendip, sendport, ttl, id, noask):
    # Check if I am busy and respond accordingly


    # If TTL > 1, send it to known hosts not in noask list
    #if (ttl > 1):
        #ttl -= 1
        # Check noask list vs known hosts list and generate list of new unique hosts

        # Send request to each unique host

    load_hosts()
    return "Test"
    #return "TO-DO: Return valid response and send requests to all other computers/programs not in noask list."