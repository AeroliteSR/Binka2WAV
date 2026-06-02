import subprocess
from pathlib import Path
import sys
import argparse
from formats import all_formats, default_formats

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", help="Files to process")
parser.add_argument("-f", "--formats", nargs="+", default=default_formats, choices=all_formats,
                    help="List of formats to check for. Separated by spaces.")
parser.add_argument("--preserve", action="store_true", help="Preserve original files after conversion.")


def get_files_from_path(path, formats):
    path = Path(path)

    if path.is_file() and path.suffix.removeprefix(".").lower() in formats:
        return [path]

    if path.is_dir():
        lst = []
        for t in formats:
            c = list(path.rglob(f"*{t}"))
            print(f"Found {len(c)} {t} files in {path}")
            lst.extend(c)

        return lst

    return []

def collect_all_files(paths, formats):
    files = []
    for path in paths:
        files.extend(get_files_from_path(path, formats))
    return files

def executeFiles(exe_path, files, PRESERVE: bool = False):
    for file in files:
        output_file = file.with_suffix(".wav")
        command = [str(exe_path), str(file), '-o', str(output_file)]
        print(subprocess.list2cmdline(command))

        try:
            subprocess.run(command, check=True)
            if PRESERVE:
                continue # skip delete if flag is set

            if output_file.exists() and output_file.stat().st_size > 0:
                file.unlink()
                print(f"Converted: {file}")
            else:
                raise RuntimeError("Process completed with no errors thrown by vgmstream, however output file is either not written or empty.\n" \
                                f"Original will be preserved in case further action is necessary: \n {file}")
            
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed: {file}")
            print(e)
        except Exception as e:
            print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    args = parser.parse_args()

    if not args.files:
        print("Drag and drop files or folders onto this executable.")
        input("Press Enter to exit...")
        sys.exit()

    exe_path = (
        Path(getattr(sys, "_MEIPASS", "."))
        / "vgmstream"
        / "vgmstream-cli.exe")

    files = collect_all_files(args.files, args.formats)

    if files:
        executeFiles(exe_path, files, args.preserve)

    else:
        print("No supported files found.")

    input("Done! Press Enter to exit...")
# pyinstaller --onefile --add-data "vgmstream;vgmstream" VGM2WAV.py