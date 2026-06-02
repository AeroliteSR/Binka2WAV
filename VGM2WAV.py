import subprocess
from pathlib import Path
import sys
import argparse
from formats import all_formats, default_formats

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", help="Files to process")
parser.add_argument("-f", "--formats", nargs="+", default=default_formats, choices=all_formats,
                    help="List of formats to check for. Separated by spaces.")


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

def executeFiles(exe_path, binka_files):
    for file in binka_files:
        command = [str(exe_path), str(file), '-o', str(file.with_suffix(".wav"))]
        print(subprocess.list2cmdline(command))

        try:
            subprocess.run(command, check=True)
            file.unlink()
            print(f"Converted: {file}")
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
        executeFiles(exe_path, files)

    else:
        print("No supported files found.")

    input("Done! Press Enter to exit...")
# pyinstaller --onefile --add-data "vgmstream;vgmstream" VGM2WAV.py