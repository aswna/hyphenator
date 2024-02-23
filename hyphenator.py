#!/usr/bin/env python3

"""
This toool helps the reading practice of Hungarian words.

It takes into account the learning order of the alphabet
used by the Meixner-method.

The words are selected from the dictionary given on the command line,
by default the filename is 'magyar-szavak.txt'.

Warning: the dictionary may contain non-existent, or inappropriate words!
"""

import argparse
import random
import re
import sys

import pyphen

MEIXNER_VOWELS = (
    ('a', 'i', 'ó'),
    ('e', 'ú'),
    ('o', 'u'),
    ('í', 'á'),
    ('ő', 'ö'),
    ('é'),
    (''),
    ('ű', 'ü'),
)

MEIXNER_CONSONANTS = (
    ('m', 't', 's'),
    ('v', 'l'),
    ('p', 'c'),
    ('k', 'f'),
    ('h', 'z'),
    ('d', 'j',),
    ('n', 'sz'),
    ('g', 'r',),
    ('b', 'gy',),
    ('cs', 'ny'),
    ('zs', 'ty'),
    ('ly', 'dz'),
    ('x', 'dzs'),
    ('y', 'w'),
    ('q'),
)

# Simple workaround for the Hungarian dictionary used by Pyphen.
# This workaround handles simple cases, but still might fail on compound words.
# See https://github.com/Kozea/Pyphen/issues/61
VOWELS = ''.join(v for level in MEIXNER_VOWELS for v in level)
START_PATTERN = re.compile(
    f'^([{VOWELS}])(([^{VOWELS}]|cs|gy|ny|sz|ty|zs)?[{VOWELS}])')
END_PATTERN = re.compile(f'([{VOWELS}])([{VOWELS}])$')


def main():
    """Start here."""
    args = parse_args()

    hyphenator = get_hyphenator()
    (consonants_pool, vowels_pool) = get_letter_pools(args)

    with open(args.dictionary, encoding='utf-8') as f:
        lines = f.readlines()

    allowed_words = get_allowed_words(lines, consonants_pool, vowels_pool)

    for count, word in enumerate(allowed_words):
        if count >= args.count:
            break

        hypenated_word = hyphenator.inserted(word)
        # See more info above!
        hypenated_word = START_PATTERN.sub('\\1-\\2', hypenated_word)
        hypenated_word = END_PATTERN.sub('\\1-\\2', hypenated_word)
        print(f'{hypenated_word}')


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--level',
                        type=int,
                        default=0,
                        help='level')
    parser.add_argument('--dictionary',
                        default='magyar-szavak.txt',
                        help='dictionary to use')
    parser.add_argument('--count',
                        type=int,
                        default=5,
                        help='maximum number of words to give')
    args = parser.parse_args()
    return args


def get_hyphenator():
    """Get hyphenator."""
    if 'hu_HU' not in pyphen.LANGUAGES:
        sys.exit('hu_HU is not supported / not installed')
    return pyphen.Pyphen(lang='hu_HU')


def get_letter_pools(args):
    """Get already learned consonants and vowels."""
    consonants_pool = set()
    vowels_pool = set()

    if args.level <= 0:
        consonants_pool.update(
            c for level in MEIXNER_CONSONANTS for c in level)
        vowels_pool.update(v for v in VOWELS)
    elif (args.level <= len(MEIXNER_CONSONANTS) or
          args.level <= len(MEIXNER_VOWELS)):
        for i in range(args.level):
            min_c = min(i, len(MEIXNER_CONSONANTS) - 1)
            consonants_pool.update(MEIXNER_CONSONANTS[min_c])
            min_v = min(i, len(MEIXNER_VOWELS) - 1)
            vowels_pool.update(MEIXNER_VOWELS[min_v])
    else:
        sys.exit('Not implemented, yet!')

    return (list(consonants_pool), list(vowels_pool))


def get_allowed_words(lines, consonants_pool, vowels_pool):
    """Get allowed words (words which contain learned letters only)."""
    allowed_words = []
    for word in lines:
        word = word.strip()
        letters = set(x for x in word)
        for letter in letters:
            if letter not in consonants_pool and letter not in vowels_pool:
                break
        else:
            if is_graph_allowed(word, consonants_pool):
                allowed_words.append(word)

    random.shuffle(allowed_words)

    return allowed_words


def is_graph_allowed(word, consonants_pool):
    """Check whether the word contains not yet learned digraphs/trigraphs."""
    for graph in ('sz', 'gy', 'cs', 'ny', 'zs', 'ty', 'ly', 'dz', 'dzs'):
        if graph in word and graph not in consonants_pool:
            return False
    return True


if __name__ == '__main__':
    main()
