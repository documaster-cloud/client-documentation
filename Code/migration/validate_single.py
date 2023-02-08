from json import decoder
from pathlib import Path
from sys import argv, exit, stderr

from pydantic import ValidationError

from models import FileImportModel

if __name__ == "__main__":

    found_error: bool = False
    for file_path in [p for p in [Path(a) for a in argv[1:]] if p.is_file()]:
        print_path = file_path.absolute()
        try:
            FileImportModel.parse_file(file_path)

        except decoder.JSONDecodeError:
            found_error = True
            stderr.write(f"File {print_path!s} is not JSON\n")

        except ValidationError as error:
            found_error = True
            stderr.write(f"\nFile {print_path!s} got validation error: \n{error!s}\n")

    exit(-1 * int(found_error))
