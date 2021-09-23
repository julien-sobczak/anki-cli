import os
import re
import yaml

from anki.storage import Collection
from anki.exporting import AnkiPackageExporter

def parse_cards(path):
  """
  Parses the input YAML file and validate the content.
  """
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

class Loader:

  def __init__(self, anki_dir, media_dir):
    self.anki_dir = anki_dir
    self.media_dir = os.path.realpath(media_dir)
    self.cwd = os.getcwd() # To restore previous path
    self._open_collection()

  def _open_collection(self):
    anki_collection_path = os.path.join(self.anki_dir, "collection.anki2")
    print("📂 Opening Anki collection...")
    self.col = Collection(anki_collection_path, log=True)

  def _add_note(self, entry, deck_id):
    model_name = entry['type']
    model = self.col.models.byName(model_name)
    self.col.decks.current()['mid'] = model['id']

    # Create a new card
    note = self.col.newNote()
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
        media_path = os.path.join(self.media_dir, filename)
        if os.path.exists(media_path):
          source_path = media_path
          print("\t- copying media file '%s'" % filename)
          self.col.media.addFile(source_path)
        else:
          print("🙈 Ignoring media file '%s'. Not found: %s" % (filename, media_path))

    # Set the tags
    if entry['tags']:
      note.tags = self.col.tags.canonify(entry['tags'])

    self.col.add_note(note, deck_id)


  def load(self, cards, deck_name="Defaut"):
    print("🔍 Loading notes into the deck '%s'..." % deck_name)

    # Set the deck
    deck = self.col.decks.byName(deck_name)
    if not deck:
      raise RuntimeError("👀 No deck named %s found." % deck_name)
    deck_id = deck['id']

    for entry in cards:
      self._add_note(entry, deck_id)

    # Save the collection
    print("💾 Saving Anki collection...")
    self.col.save()
    os.chdir(self.cwd)

  def export(self, archive_file):
    # Exporting the collection
    e = AnkiPackageExporter(self.col)
    e.exportInto(archive_file)
