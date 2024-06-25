import sys
from edk2_helper import Edk2Helper, Edk2HelperError
from arg_parser import parse_args

def new() -> None:
    pass

def main() -> int:
    eh = Edk2Helper(parse_args())
    try:
        eh.exec()
    except Edk2HelperError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
