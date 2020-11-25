# Anki CLI

CLI to automate Anki notes creation.

**This project is not part of the official Anki project.**

## Installation

```shell
$ pip3 install anki-cli-unofficial
```

## Usage

The CLI supports a single command `load`.

```shell
$ anki-cli-unofficial load -h
usage: __main__.py load [-h] [--anki-home ANKI_HOME] [--media-dir MEDIA_DIR]
                        [--deck DECK]
                        input

positional arguments:
  input                 file containing the flashcards to create

optional arguments:
  -h, --help            show this help message and exit
  --anki-home ANKI_HOME
                        Anki directory
  --media-dir MEDIA_DIR
                        path to directory containing medias references in input file
  --deck DECK           deck name in which to create flashcards
```

I recommend that you don't test this script on your Anki directory. This code may become outdated and I don't want bugs to damage your precious flashcards.
Therefore, before running this program, make sure to create a sandbox environment:

* On Windows: `"C:\Program Files\Anki\anki.exe" -b "%PWD%/AnkiTest"`
* On MacOS: `open /Applications/Anki.app --args -b $PWD/AnkiTest`
* On Linux: `anki -b $PWD/AnkiTest`

These commands create a new Anki directory. For now, simply close Anki. The CLI will interact with this directory and Anki must not be running at the same time.

The command `load` expects a YAML file as input following this format:

```yaml
# File cards.yaml

# An array of documents

- type: Basic # The type of the node to create ("Basic", "Basic (with reverse card)", etc.). Also known as the model.
  tags: [tag1, tag2] # An optional list of tags
  fields: # The ordered list of field for the selected note type (ex: Basic notes require two fields: Front & Back)
    Front: Bonjour
    Back: Hello
```

Then, to load this file into Anki:

```shell
$ anki-cli-unofficial load cards.yaml
```

Reopen Anki using the same command as before. You must see your new flashcards! Export them using the Anki button and import them in your real collection. That's it!

## Advanced Uses

### Medias

Medias are supported using the usual Anki syntax:

* Include `[sound:file.mp3]` inside a field to add sounds to your flashcard.
* Include `<img src="file.jpg">` inside a field to add images to your flashcard.

Ex:

```yaml
- type: Basic
  fields:
    Front: '<img src="car.jpg" />'
    Back: '[sound:voiture.mp3] Une voiture'
# This card will show the picture of a card and print the translation
# with the pronunciation when the back card is revealed.
```


You must specify the local directory containing the media files. The CLI will copy these files in Anki medias database (missing files are ignored).

```shell
$ anki-cli-unofficial load --media-dir ~/anki-images cards.yaml
# Where ~/anki-images contains the files car.jpg and voiture.mp3
```

## Examples

You will find additional examples in the directory `examples/`.


## Test locally (for developers)

```shell
$ cd anki-cli/
$ python3 setup.py install # The binary anki-cli-unofficial is now present in $PATH
$ anki-cli-unofficial load --media-dir $PWD/Workshop/anki-cli/examples $PWD/Workshop/anki-cli/examples/french.yaml
```

## Uploading to Pypi

1. Create an API Token from the Web UI. (Edit your `~/.pypirc` with the generated token.)
2. Install Twine
```shell
$ python3 -m pip install --user --upgrade twine
```
3. Upload the bundle
```shell
$ python3 -m twine upload dist/*
```

Note: The upload to Pypi is currently assured by GitHub Actions.
