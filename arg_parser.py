from pathlib import Path
from argparse import ArgumentParser, Namespace
from constants import PROG, VERSION, COMMANDS, NEW_TYPES, PACKAGE

def parse_args() -> Namespace:
    ap = ArgumentParser(
        prog=PROG,
        allow_abbrev=False,
        description=f"Edk2 Helper {VERSION}"
    )
    ap.add_argument(
        '-V',
        '--version',
        action='version',
        version=VERSION,
    )
    sp = ap.add_subparsers(
        dest='cmd',
        required=True,
        metavar="command",
        help=(
            f"one of: {', '.join(COMMANDS)}. "
            f"Try `{PROG} <command> --help' for help on specific command."
        ),
    )

    new = sp.add_parser(
        'new',
        description=(
            "Create a module, library, or package with some boilerplate code. "
            f"For example, command `{PROG} new m Foo -o ExamplePkg/Universal' "
            "creates `ExamplePkg/Universal/Foo/Foo.inf', and command "
            f"`{PROG} new p AnotherPkg' creates `AnotherPkg/AnotherPkg.dec'. "
        ),
        allow_abbrev=True,
    )
    keywords = ', '.join(NEW_TYPES.keys())
    descriptions = ', '.join(NEW_TYPES.values())
    new.add_argument(
        'type',
        choices=NEW_TYPES,
        metavar="type",
        help=f"one of: {keywords} ({descriptions})",
    )
    new.add_argument(
        'name',
        help="base name of the new item, directory, and files",
    )
    new.add_argument(
        '-o',
        '--location',
        type=Path,
        help=(
            "path to the parent directory of the new item, required if type "
            "is not package"
        ),
    )
    new.add_argument(
        '-p',
        '--parents',
        action='store_true',
        help="create non-existent parent directories if needed",
    )
    args = ap.parse_args()
    if args.location is None:
        if args.type == PACKAGE[0:1]:
            args.location = Path.cwd()
        else:
            ap.error("-o/--location is required if type is not package")
    return args
