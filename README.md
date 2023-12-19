# Overview / Leírás
This tool helps the reading practice of Hungarian words,
taking into account the learning order of the alphabet
used by the Meixner-method.

The words are selected from the dictionary given on the command line,
by default this filename is ``magyar-szavak.txt``.

Warning: the dictionary may contain non-existent, or inappropriate words!

Ez az eszköz a magyar szavak szótagolva olvasását segíti,
figyelembe vevé a Meixner-módszer ábécéjének tanulási sorrendjét.

A program a szavakat a parancssorban megadott szótárból használja,
ez alapesetben a ``magyar-szavak.txt`` nevű fájl.

Figyelem: a szótár nem létező és nem kívánatos szavakat is tartalmazhat!

```
$ ./hyphenator.py --help
usage: hyphenator.py [-h] [--level LEVEL] [--dictionary DICTIONARY] [--count COUNT]

options:
  -h, --help            show this help message and exit
  --level LEVEL         level (default: 0)
  --dictionary DICTIONARY
                        dictionary to use (default: magyar-szavak.txt)
  --count COUNT         maximum number of words to give (default: 5)
```

# Example / Példa
```
$ ./hyphenator.py --level 3 --count 3
ma-ma
i-tal-lap
tem-pós

$ ./hyphenator.py
meg-nyi-tó-ün-ne-pély
ér-zés-sel
be-le-idéz
hir-de-tés-szö-veg
meny-nyi-en
```
