# Anki CLI

**This project is not part of the official Anki project.**


## Installation

```shell
$ pip3 install anki-cli-unofficial
$ anki-cli-unofficial -h
# To load a local file cards.yaml into the default deck
$ anki-cli-unofficial --deck Default cards.yaml
```

## Test locally

```shell
$ pip3 install anki-cli-unofficial
$ python3 anki-cli-unofficial/ load --deck Default --media-dir examples examples/french.yaml
```

```shell
$ cd anki-cli/
$ python3 setup.py install # The binary anki-cli-unofficial is present in $PATH
$ cd
$ anki-cli-unofficial load --media-dir $PWD/Workshop/anki-cli/examples $PWD/Workshop/anki-cli/examples/french.yaml
```
