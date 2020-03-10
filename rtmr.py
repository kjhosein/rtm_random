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
    parser = argparse.ArgumentParser(description='Get a random TO DO from RTM!', prefix_chars='-/')
    parser.add_argument('--loglevel', dest='loglevel', metavar='',
                        choices=['debug'], type=str.lower,
                        help="[optional] Set the log level (e.g. debug, etc.)")
    args = parser.parse_args(raw_args)

    # Set loglevel if --loglevel argument is used, otherwise set to INFO:
    # if args.loglevel is not None:
    if args.loglevel is None:
        logging_num_level = 20
    else:
        logging_num_level = getattr(logging, args.loglevel.upper())

    LOG_FORMAT = "\n %(levelname)s: %(message)s"
    logging.basicConfig(level=logging_num_level, format=LOG_FORMAT)

    logging.debug("Args passed in are: " + str(args))

    user_home_dir = os.path.expanduser("~")
    rtm_auth_file = os.path.join(user_home_dir, '.rtm_auth_token')
    if os.path.exists(rtm_auth_file):
        with open(rtm_auth_file, "r") as f:
            token = f.readline()
    else:
        token = None

    api = Rtm(api_key, shared_secret, "read", token)

    # authenication block, see http://www.rememberthemilk.com/services/api/authentication.rtm
    # check for valid token
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

        # user_home_dir = expanduser("~")
        # rtm_auth_file = os.path.join(user_home_dir, '.rtm_auth_token')
        f = open(rtm_auth_file, "w")
        f.write(api.token)
        f.close()

    # get all open tasks, see http://www.rememberthemilk.com/services/api/methods/rtm.tasks.getList.rtm
    result = api.rtm.tasks.getList(filter="status:incomplete list:Current priority:1 ")
    list_of_tasks = []

    for tasklist in result.tasks:
        for taskseries in tasklist:
            list_of_tasks.append(taskseries.name)
    random_task_name = random.choice(list_of_tasks)
    print '# of tasks is: ', len(list_of_tasks)

    logging.debug("Random task name is: " + random_task_name)

    # Get only the specific task by task_id
    result = ""
    result = api.rtm.tasks.getList(filter="name:%s" % random_task_name)
    for tasklist in result.tasks:
        for taskseries in tasklist:
            print 'Task Name: \t', COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, taskseries.name, Style.RESET_ALL
            print 'Priority: \t', COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, taskseries.task.priority, Style.RESET_ALL
            logging.debug('The type of taskseries.task.due is ...' + str(type(taskseries.task.due)))
            if taskseries.task.due == '':
                print 'Due: \t\t-'
            else:
                formatted_date = strftime(strptime(taskseries.task.due, "%Y-%m-%dT%H:%M:%SZ"), "%d %b %Y")
                print 'Due: \t\t', COLORAMA_STYLE, COLORAMA_BG, COLORAMA_FG, formatted_date, Style.RESET_ALL
    print


if __name__ == '__main__':
    main()
