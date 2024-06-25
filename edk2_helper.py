from uuid import uuid4
from pathlib import Path
from constants import NEW_TYPES, MODULE, LIBRARY, PACKAGE

class Edk2Helper:
    def __init__(
            self,
            args,
    ) -> None:
        self.args = args
        self.func = getattr(self, f'_cmd_{args.cmd.replace('-', '_')}')

    def exec(self) -> None:
        self.func()

    def _cmd_new(self) -> None:
        new_type: str = NEW_TYPES[self.args.type]
        name: str = self.args.name
        location: Path = self.args.location
        parents: bool = self.args.parents
        try:
            (new_dir := location / name).mkdir(parents=parents, exist_ok=True)
        except FileNotFoundError:
            raise Edk2HelperError(
                f"location ({location.resolve()}) does not exist, either "
                "specify -p/--parents, or create it manually"
            ) from None
        new_file = (new_dir / name).with_suffix('.dec' if new_type == PACKAGE else '.inf')

        if new_type == PACKAGE:
            content = (
                '[Defines]\n'
                '  DEC_SPECIFICATION = 0x00010019\n'
                f'  PACKAGE_NAME      = {name}\n'
                f'  PACKAGE_GUID      = {uuid4()}\n'
                '  PACKAGE_VERSION   = 1.0\n'
            )
        else:
            content = (
                '[Defines]\n'
                '  INF_VERSION       = 0x0001001B\n'
                f'  BASE_NAME         = {name}\n'
                f'  FILE_GUID         = {uuid4()}\n'
                '  MODULE_TYPE       = BASE\n'
                '  VERSION_STRING    = 1.0\n'
            )
            if new_type == MODULE:
                content += f'  ENTRY_POINT       = {name}Entry\n'
            if new_type == LIBRARY:
                content += f'  LIBRARY_CLASS     = {name}\n'

        try:
            with new_file.open('x', encoding='utf-8', newline='\r\n') as f:
                f.write(content)
        except FileExistsError:
            raise Edk2HelperError(f"file already exists: {new_file}") from None


class Edk2HelperError(Exception):
    pass
