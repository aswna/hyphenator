#!/usr/bin/env python3

"""This is a tool to practice reading considering the Meixner-method."""

import argparse
import os
import random
import sys

import pyphen

MEIXNER_VOWELS = (
    ('a', 'i', 'ó'),
    ('e', 'ú'),
    ('o', 'u'),
    ('í', 'á'),
    ('ő', 'ö'),
    ('é'),
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

        # this might not be complete
        hypenated_word = hyphenator.inserted(word)
        # print(hypenated_word)

        # this still might not be complete, but handles simple cases
        # (might fail on compound words)
        vowels = 'aáeéiíoóöőuúüű'
        os.system(
            f"echo {hypenated_word} | sed "
            f"'s/^\\([{vowels}]\\)\\(\\([^{vowels}]"
            f"\\|cs\\|gy\\|ny\\|sz\\|ty\\|zs\\)\\?"
            f"[{vowels}]\\)/\\1-\\2/;"
            f"s/\\([{vowels}]\\)\\([{vowels}]\\)$/\\1-\\2/'")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--level", type=int, default=0,
                        help="level")
    parser.add_argument("--dictionary", default="magyar-szavak.txt",
                        help="dictionary to use")
    parser.add_argument("--count", type=int, default=5,
                        help="maximum number of words to give")
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
        vowels_pool.update(v for level in MEIXNER_VOWELS for v in level)
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
        # print(f'letters = {letters}')
        for letter in letters:
            if letter not in consonants_pool and letter not in vowels_pool:
                break
        else:
            if is_graph_allowed(word, consonants_pool):
                allowed_words.append(word)
    # print(f'number of allowed_words = {len(allowed_words)}')
    # for word in allowed_words:
    #     print(word)

    random.shuffle(allowed_words)

    return allowed_words


def is_graph_allowed(word, consonants_pool):
    """Check whether the word contains not yet learned digraphs/trigraphs."""
    # check for digraphs and trigraph(s)
    for graph in ('sz', 'gy', 'cs', 'ny', 'zs', 'ty', 'ly', 'dz', 'dzs'):
        if graph in word and graph not in consonants_pool:
            return False
    return True


if __name__ == '__main__':
    main()
