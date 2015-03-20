

"""svyn.svyn: provides entry point main()."""


__version__ = "0.1.0"

from .svynworker import SvynWorker, SvynError

# Standard library
import argparse
import ConfigParser
import os
import sys


MESSAGE_MISSING_CONFIG = "Config file expected at ~/.svynrc not found."
MESSAGE_UNABLE_TO_SWITCH = "Unable to switch: {}"


def init_optparser():
    p = argparse.ArgumentParser(
        description="Convenience wrapper for svn functions.")
    p.add_argument("--version", action="version", version="0.1.0")
    p.add_argument(
        "--config",
        "-c",
        default="default",
        help="Config section to use for repo paths."
    )

    subs = p.add_subparsers(title="commands")

    branch_p = subs.add_parser(
        "branch",
        help="Create svn cp of copy_target to branches/<NAME> with default "
             "message."
    )
    branch_p.add_argument(
        "-s",
        "--switch",
        help="Switch working directory to new branch.",
        action="store_true",
        default=False
    )
    branch_p.add_argument(
        "-m",
        "--message",
        help="Add an additional message describing branch."
    )
    branch_p.add_argument(
        "name",
        help="Intended name of new branch."
    )
    branch_p.set_defaults(func=branch)

    tag_p = subs.add_parser(
        "tag",
        help="Create copy of trunk at given rev to tags_dir"
    )
    tag_p.add_argument(
        "trunk_rev",
        help="The trunk revision to tag from."
    )
    tag_p.add_argument(
        "version",
        help="The version of the tag."
    )
    tag_p.set_defaults(func=tag)

    list_p = subs.add_parser(
        "list",
        help="Lists current branches. Optionally search in them with -s"
    )
    list_p.add_argument(
        "-s",
        "--search",
        help="String to search directory names for."
    )
    list_p.add_argument(
        "-m",
        "--mine",
        action="store_true",
        default=False,
        help="Filter listed branches to those where current user is "
             "last author."
    )
    list_p.set_defaults(func=list)

    return p


def init_config():
    """Expects a .svynrc in home folder."""
    cp = ConfigParser.SafeConfigParser()
    try:
        with open(os.path.expanduser("~/.svynrc")) as config:
            cp.readfp(config)
    except IOError:
        print MESSAGE_MISSING_CONFIG
        sys.exit(1)
    return cp


def main():
    p = init_optparser()
    c = init_config()
    args = p.parse_args()
    s = SvynWorker(dict(c.items(args.config)))
    # Execute command with options and arguments.
    args.func(s, args)


def branch(s, args):
    branch = s.branch(args.name, args.message)
    if args.switch:
        try:
            s.switch(os.getcwd(), branch)
        except SvynError as e:
            print MESSAGE_UNABLE_TO_SWITCH.format(repr(e))
            sys.exit(1)


def tag(s, args):
    pass


def list(s, args):
    branches = s.list(args.search, args.mine)
    for b in branches:
        print b


def overlap(s, args):
    pass
