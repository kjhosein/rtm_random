#!/usr/bin/env python2

import os
import sys
import random
import logging
import argparse
from datetime import datetime
import webbrowser
from rtmapi import Rtm
from colorama import init
from colorama import Fore, Back, Style
from time import sleep
from progress.spinner import Spinner


init()  # allows colorama to work under Windows

# The next 2 lines are workarounds for a bug in the datetime module.
# reference: https://stackoverflow.com/a/43043036/389946
strptime = datetime.strptime
strftime = datetime.strftime

api_key = "98cfa8464ef953428bc3a8cce7f6f155"
shared_secret = "9da203dc006ffcc3"

# Highlighting Colors (uses Colorama module):
# Options:
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT
FG = "CYAN"
BG = "RESET"
STYLE = "BRIGHT"
COLORAMA_FG = getattr(Fore, FG)
COLORAMA_BG = getattr(Back, BG)
COLORAMA_STYLE = getattr(Style, STYLE)


def main(raw_args=None):
    # Check the arguments passed to this script
    parser = argparse.ArgumentParser(description='Get a random TO DO from Remember the Milk!', prefix_chars='-/',
                                     epilog='Note that multiple flags are ANDed together making your search more specific. See docs for more info.')
    parser.add_argument('--loglevel', dest='loglevel', metavar='',
                        choices=['debug'], type=str.lower,
                        help="[optional] Set the log level (e.g. debug, etc.)")
    parser.add_argument('-l', '--list', metavar='',
                        help="[optional] Select a specific list to search in. Use quotes if your list name has spaces in it.")
    parser.add_argument('-t', '--tag', metavar='',
                        help="[optional] Select a specific tag to add to your search filter.")
    parser.add_argument('-p', '--priority', metavar='', choices=['1', '2', '3', 'N'],
                        help="[optional] Select a specific priority to add to your search filter.")
    args = parser.parse_args(raw_args)

    # Set loglevel if --loglevel argument is used, otherwise set to INFO
    if args.loglevel is None:
        logging_num_level = 20
    else:
        logging_num_level = getattr(logging, args.loglevel.upper())

    LOG_FORMAT = "\n %(levelname)s: %(message)s"
    logging.basicConfig(level=logging_num_level, format=LOG_FORMAT)

    logging.debug("Args passed in are: " + str(args))

    rtm_list = args.list
    rtm_tag = args.tag
    rtm_priority = args.priority

    # Look for a token in ~/.rtm_auth_token first
    user_home_dir = os.path.expanduser("~")
    rtm_auth_file = os.path.join(user_home_dir, '.rtm_auth_token')
    if os.path.exists(rtm_auth_file):
        with open(rtm_auth_file, "r") as f:
            token = f.readline()
    else:
        token = None

    # Create a class instance using the RtmAPI module
    api = Rtm(api_key, shared_secret, "read", token, api_version=2)

    # Authenication block, see http://www.rememberthemilk.com/services/api/authentication.rtm
    # Check for valid token. If none, open a browser so the user can authenticate.
    if not api.token_valid():
        # use desktop-type authentication
        url, frob = api.authenticate_desktop()
        # open webbrowser, wait until user authorized application
        webbrowser.open(url)
        raw_input("Continue?")
        # get the token for the frob
        api.retrieve_token(frob)
        # print out new token, should be used to initialize the Rtm object next time
        # (a real application should store the token somewhere)
        logging.debug("New token: %s" % api.token)

        # Write out the token to the user's home directory
        f = open(rtm_auth_file, "w")
        f.write(api.token)
        f.close()

    # Get all incomplete tasks based on the constructed filter.
    # RTM filters: https://www.rememberthemilk.com/help/?ctx=basics.search.advanced
    filter = 'status:incomplete isSubtask:false'
    if rtm_list:
        filter = filter + ' list:"%s"' % rtm_list
    if rtm_tag:
        filter = filter + ' tag:"%s"' % rtm_tag
    if rtm_priority:
        filter = filter + ' priority:"%s"' % rtm_priority

    logging.debug("filter is now: " + filter)
    result = api.rtm.tasks.getList(filter="%s" % filter)
    list_of_tasks = []

    # Use the RtmAPI tasks iter to put the filtered set of tasks into a list
    for tasklist in result.tasks:
        for taskseries in tasklist:
            list_of_tasks.append(taskseries.name)

    # Pick out a random task name
    random_task_name = random.choice(list_of_tasks)
    logging.debug("Random task name is: " + random_task_name)

    # Use the random task's name to retrieve its full info
    result = ""
    result = api.rtm.tasks.getList(filter='name:"%s"' % random_task_name)
    logging.debug("results.tasks has a type of: " + str(type(result.tasks)))

    # Use the RtmAPI iterators to drill down to the taskseries & task info.
    # To better understand what's going on here, you'll need to read the
    # RtmAPI docs as well as how Remember The Milk's API returns queries.
    first_tasklist = iter(result.tasks).next()
    logging.debug("tasklist has a type of: " + str(type(tasklist)))

    first_taskseries = iter(first_tasklist).next()
    logging.debug("first_taskseries  type is: " + str(type(first_taskseries)))

    spinner()  # Cosmetic only ;-)

    print "\nTask Name: \t", COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, first_taskseries.name, Style.RESET_ALL

    if "N" in first_taskseries.task.priority:
        print 'Priority: \t', COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, 'None', Style.RESET_ALL
    else:
        print 'Priority: \t', COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, first_taskseries.task.priority, Style.RESET_ALL

    if first_taskseries.task.due == '':
        print 'Due: \t\t -'
    else:
        formatted_date = strftime(strptime(first_taskseries.task.due, "%Y-%m-%dT%H:%M:%SZ"), "%d %b %Y")
        print 'Due: \t\t', COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, formatted_date, Style.RESET_ALL

    # As a bonus, print the # of tasks in the user's search filter
    print "\n PS: The total # of tasks with your search filter is: ", COLORAMA_STYLE, \
        COLORAMA_BG, COLORAMA_FG, len(list_of_tasks), Style.RESET_ALL, "\n"


def spinner():
    # Just a little bit of flash. Has no true functionality, apart from
    # possibly some psychological lift.
    print

    spinner = Spinner("Fetching tasks ")
    for i in range(16):
        spinner.next()
        sleep(0.1)
    spinner.finish()

    spinner = Spinner("\rPicking a random task ")
    for i in range(16):
        spinner.next()
        sleep(0.1)
    spinner.finish()

    print "Here you go!"


if __name__ == '__main__':
    main()
