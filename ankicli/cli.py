import argparse
import os
from pathlib import Path
import platform
import tempfile
import sys

from .loader import Loader, parse_cards

try:
  import anki
except ImportError:
  raise RuntimeError("Python anki package is not installed. Please run:\n\t$ pip3 install anki==<your_version>")

def get_anki_dir_default():
  # Anki home directory depends on the platform
  # See https://docs.ankiweb.net/#/files?id=file-locations
  plt = platform.system()
  home = str(Path.home())

  directory = None
  if plt == "Windows":
    directory = os.path.join(os.getenv('APPDATA'), 'Anki2')
  elif plt == "Linux":
    directory = os.path.join(home, '.local/share/Anki2')
  elif plt == "Darwin":
    directory = os.path.join(home, 'Library/Application Support/Anki2')

  if not directory:
    raise RuntimeError("❌ Failed to detect your OS. Only Windows/Linux/MacOS are supported.")

  return directory

def get_anki_command():
  # Anki home directory depends on the platform
  # See https://docs.ankiweb.net/#/files?id=startup-options
  plt = platform.system()
  if plt == "Windows":
    return '"C:\Program Files\Anki\anki.exe"'
  elif plt == "Linux":
    return "anki"
  elif plt == "Darwin":
    return "open /Applications/Anki.app --args"
  else:
    raise RuntimeError("❌ Failed to detect your OS. Only Windows/Linux/MacOS are supported.")

def main():
  parser = argparse.ArgumentParser(prog='anki-cli-unofficial')
  subparsers = parser.add_subparsers(title='subcommands',
                                     description='valid subcommands',
                                     help='additional help')
  import_parser = subparsers.add_parser('load')
  import_parser.add_argument('--anki-dir', default=None, nargs="+", help="Anki user directory (Default to a temp directory)")
  import_parser.add_argument('--media-dir', default=".", help="local directory containing medias referenced in input_file")
  import_parser.add_argument('--deck', default="Default", help="deck name in which to create flashcards")
  import_parser.add_argument('input_file', help="file containing the flashcards to create")
  import_parser.add_argument('output_file', help="Anki generated archive filepath")
  args = parser.parse_args()


  # Check the input file exists
  if not os.path.isfile(args.input_file):
    print("❌ Input file %s doesn't exist." % args.input_file)
    print("👋 Exiting...")
    sys.exit(1)

  # Parse the input file
  cards = parse_cards(args.input_file)

  # Check the medias directory exists
  media_dir_normalized = os.path.normpath(os.path.expanduser(args.media_dir))
  if not os.path.isdir(media_dir_normalized):
    print("❌ Media directory %s doesn't exist." % args.media_dir)
    print("👋 Exiting...")
    sys.exit(1)

  # Check the Anki home path exists
  anki_dir = args.anki_dir
  anki_dir_new = None
  if not anki_dir:
    # Use a temp dir for Anki home
    anki_dir_root = tempfile.mkdtemp()
    anki_dir = os.path.join(anki_dir_root, 'User 1')
    os.mkdir(anki_dir, 0o755)
    anki_dir_new = True
  else:
    anki_dir_new = False
    # Path is provided. We expect the directory to exist.
    anki_dir = os.path.normpath(os.path.expanduser(' '.join(args.anki_dir)))
    if not os.path.isdir(anki_dir):
      print("❌ Anki directory %s doesn't exist." % anki_dir)
      print("👋 Exiting...")
      sys.exit(1)

    # We expect a file collection.anki2 in this directory
    anki_collection_file = os.path.join(anki_dir, 'collection.anki2')
    if not os.path.isfile(anki_collection_file):
      print("❌ Anki collection file %s doesn't exist." % anki_collection_file)
      print("👋 Exiting...")
      sys.exit(1)

    anki_dir_default = os.path.realpath(get_anki_dir_default())
    if anki_dir.startswith(anki_dir_default):
      # Ask confirmation before continuing
      print("🔥🔥🔥 You are using your current Anki collection. This is NOT recommended. Bugs happens 🐛🐛🐛.")
      answer = input("Continue? (yes/no): ")
      if answer != "yes":
        print("👋 Exiting...")
        sys.exit(0)

  anki_path = Path(anki_dir)
  loader = Loader(anki_dir, media_dir_normalized)
  loader.load(cards, args.deck)
  print("👍 Done")
  print("👉 Anki collection can be opened using the following command:\n\t%s -b %s" % (get_anki_command(), anki_path.parent))

  if not anki_dir_new:
    answer = input("🔥 You are working on an existing collection. Exporting it could take a long time. Continue (yes/no)? ")
    if answer != 'yes':
        print("🙊 Skipped the archive file generation")
        print("👋 Exiting...")
        sys.exit(0)

  archive_file = os.path.join(os.getcwd(), args.output_file)
  # Check the archive doesn't exist
  if os.path.isfile(archive_file):
    answer = input("🧨 Archive file %s already exists. Override (yes/no)? " % archive_file)
    if answer != 'yes':
      print("🙊 Skipped the archive file generation")
      print("👋 Exiting...")
      sys.exit(0)

  loader.export(archive_file)
  print("👉 Anki Archive is available here: %s" % archive_file)
