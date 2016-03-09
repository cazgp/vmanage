#!/usr/bin/env python
import argparse
import os, sys
import shelve
from subprocess import call

# Get a list of all known vagrants
vagrants = os.popen("vagrant global-status | sed '/^ $/Q' | tail -n +3 | awk '{print $5}'").readlines()
vagrants = [v.strip() for v in vagrants]

# Open our store to see if the user has named any of the vagrants
store_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".names")
store = shelve.open(store_path)

# Work out any custom names we may have
names = {}
for v in vagrants:
    try:
        name = store[v]
    except KeyError:
        name = v
    names[name] = v


# Given a path, check against all known vagrant paths
def check_is_vagrant(path):
    for v in vagrants:
        # Get the len of the vagrant
        len_v = len(v)
        truncated_path = path[:len_v]
        if truncated_path == v:
            return v
    return False


# Action for 'name' subparser
def action_name(args):
    cd = os.getcwd()
    is_vagrant = check_is_vagrant(cd)
    if not is_vagrant:
        print("Must be in Vagrant directory")
        sys.exit(1)
    store[v] = args.name
    print("Current vagrant box named %s" % args.name)


# Action for 'vagrant' subparser
def action_vagrants(args):
    box = names[args.box]
    os.chdir(box)
    call(["vagrant", args.action])


# Set up the parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Rename the current vagrant
# Must be called from within a vagrant thing
parser_custom_name = subparsers.add_parser("name", help="Give this vbox a custom name")
parser_custom_name.add_argument("name", help="Name to give this vbox")
parser_custom_name.set_defaults(func=action_name)

for n in names.keys():
    sub = subparsers.add_parser(n, help="Manage %s" % n)
    sub.add_argument("action", choices=["up", "halt", "ssh"], help="Vagrant action to take")
    sub.set_defaults(box=n)
    sub.set_defaults(func=action_vagrants)

args = parser.parse_args()
args.func(args)
