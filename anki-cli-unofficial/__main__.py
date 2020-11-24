import os
import argparse
import platform
import sys
from pathlib import Path

from . import loader

try:
  import anki
except ImportError:
  raise RuntimeError("Python anki package is not installed. Please run:\n\t$ pip3 install anki==<your_version>")

def get_anki_home_default():
  # Anki home directory depends on the platform
  # See https://docs.ankiweb.net/#/files?id=file-locations
  plt = platform.system()
  home = str(Path.home())

  directory = None
  if plt == "Windows":
    directory = os.path.join(os.getenv('APPDATA'), 'Anki2/User 1')
  elif plt == "Linux":
    directory = os.path.join(home, '.local/share/Anki2/User 1')
  elif plt == "Darwin":
    directory = os.path.join(home, 'Library/Application Support/Anki2/User 1')

  if not directory:
    raise RuntimeError("Failed to detect your OS. Only Windows/Linux/MacOS are supported.")

  if not os.path.isdir(directory):
    raise RuntimeError("Failed to find your Anki home directory: %s" % directory)

  return directory


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(title='subcommands',
                                     description='valid subcommands',
                                     help='additional help')
  import_parser = subparsers.add_parser('load')
  import_parser.add_argument('--anki-home', default="~/AnkiTest/User 1", help="Anki directory")
  import_parser.add_argument('--media-dir', default=".", help="path to directory containing medias references in input file")
  import_parser.add_argument('--deck', default="Default", help="deck name in which to create flashcards")
  import_parser.add_argument('input', help="file containing the flashcards to create")
  args = parser.parse_args()

  # Check the Anki home path exists
  anki_home_normalized = os.path.normpath(os.path.expanduser(args.anki_home))
  if not os.path.isdir(anki_home_normalized):
    print(anki_home_normalized)
    print("❌ Anki directory %s doesn't exist." % args.anki_home)
    print("👋 Exiting...")
    sys.exit(1)
  # Check the medias directory exists
  media_dir_normalized = os.path.normpath(os.path.expanduser(args.media_dir))
  if not os.path.isdir(media_dir_normalized):
    print("❌ Media directory %s doesn't exist." % args.media_dir)
    print("👋 Exiting...")
    sys.exit(1)

  # Check the input file exists
  if not os.path.isfile(args.input):
    print("❌ Input file %s doesn't exist." % args.input)
    print("👋 Exiting...")
    sys.exit(1)

  anki_home_default = get_anki_home_default()
  anki_home_default_normalized = os.path.realpath(anki_home_default)
  if anki_home_normalized == anki_home_default_normalized:
    # Ask confirmation before continuing
    print("🔥🔥🔥 You are using your current Anki collection. This is NOT recommended. Bugs happens 🐛🐛🐛. ")
    answer = input("Continue? (yes/no): ")
    if answer != "yes":
      print("👋 Exiting...")
      sys.exit(0)

  loader.load(anki_home_normalized, media_dir_normalized, args.input, args.deck)
  print("👍 Done")

