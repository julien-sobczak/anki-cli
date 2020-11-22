import os
import platform
from pathlib import Path
import argparse

import loader

try:
  from anki.storage import Collection
except ImportError:
  raise RuntimeError("Python anki package is not installed. Please run:\n\t$ pip3 install anki==<your_version>")


def anki_home_default():
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


def open_anki():
  # Find our Anki application
  anki_home = anki_home_default()
  # Note 1: Relative paths are not supported
  anki_collection_path = os.path.join(anki_home, "collection.anki2")

  col = Collection(anki_collection_path, log=True)

  # Find the model to use (Basic, Basic with reversed, ...)
  modelBasic = col.models.byName('Basic')
  # Set the deck
  deck = col.decks.byName('Default')
  col.decks.select(deck['id'])
  col.decks.current()['mid'] = modelBasic['id']

  # note = col.newNote()
  # note.fields[0] = "Bonjour" # The Front input field in the UI
  # note.fields[1] = "Hello"   # The Back input field in the UI
  # col.addNote(note)

  col.save()

def main():

  open_anki()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(title='subcommands',
                                     description='valid subcommands',
                                     help='additional help')
  import_parser = subparsers.add_parser('load')
  import_parser.add_argument('--deck', default="Default", help="deck name in which to create flashcards")
  import_parser.add_argument('input', help="file containing the flashcards to create")
  args = parser.parse_args()

  loader.load(args.input, args.deck)

