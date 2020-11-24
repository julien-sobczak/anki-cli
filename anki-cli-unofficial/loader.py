import os
import yaml
import re

from anki.storage import Collection

def load_flashcards_file(path):
  cards = []

  with open(path) as file:
    cards = yaml.full_load(file)

  # Validate the cards to avoid opening the Anki collection if there is no card to load.
  for card in cards:
    if 'type' not in card:
      raise RuntimeError("Attribute 'type' is required in card definition")
    if 'tags' not in card:
      card['tags'] = []
    if 'fields' not in card:
      raise RuntimeError("Attribute 'fields' is required in card definition")

  return cards

def add_note(col, media_dir, entry):
  model_name = entry['type']
  model = col.models.byName(model_name)
  col.decks.current()['mid'] = model['id']

  # Create a new card
  note = col.newNote()
  fields = entry['fields']
  for i, field in enumerate(fields):
    note.fields[i] = fields[field]

  # Upload the medias
  for name, value in fields.items():
    # Extract filenames
    sounds = re.findall(r'(?i)\[sound:(.*?)\]', value)
    images = re.findall(r'(?i)<img\s+src="(.*?)"\s*/>', value)

    # Copy medias
    for filename in sounds + images:
      media_path = os.path.join(media_dir, filename)
      if os.path.exists(media_path):
        source_path = media_path
        print("\t- copying media file %s" % filename)
        col.media.addFile(source_path)
      else:
        print("🙈 Ignoring media file %s. Not found: %s" % (filename, media_path))

  # Set the tags
  if entry['tags']:
    note.tags = col.tags.canonify(entry['tags'])

  col.addNote(note)


def load(anki_home, media_dir, file, deck="Defaut"):
  print("👉 Loading '%s' into the deck '%s'..." % (file, deck))

  # Read the cards to load
  cards = load_flashcards_file(file)

  # Open the Anki collection
  cwd = os.getcwd() # To restore previous path
  media_dir = os.path.realpath(media_dir)
  anki_collection_path = os.path.join(anki_home, "collection.anki2")
  col = Collection(anki_collection_path, log=True)

  # Set the deck
  deck = col.decks.byName(deck)
  if not deck:
    raise RuntimeError("👀 No deck named %s found." % deck)
  col.decks.select(deck['id'])

  for entry in cards:
    add_note(col, media_dir, entry)

  # Save the collection
  print("💾 Saving Anki collection...")
  col.save()
  os.chdir(cwd)



