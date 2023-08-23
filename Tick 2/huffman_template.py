#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# huffman.py
# (c) Frank Stajano 2022-12-14
# $Id: huffman_template.py 70 2023-02-03 15:50:45Z fms27 $


"""Huffman compression of a sequence of fixed-size symbols.

In this toy implementation, the fixed-size symbols to be encoded are
bytes and the variable-length codewords are bitstrings from the
community-contributed bitstring module (not in Python's standard
library):

available at
  https://github.com/scott-griffiths/bitstring/

documented at
  https://bitstring.readthedocs.io/en/stable/index.html

installable through
  pip install bitstring

Throughout this code we must make and maintain a clear distinction
between bytes and small integers. There is obviously a 1-to-1 mapping
between the integers 0..255 and the possible values for a byte, but a
byte is not an integer and a small integer is not a byte. Our
convention is that we represent the symbols of the sequence to be
encoded as Python bytes at all times. If we sometimes used them as
integers, we would be able to store some lookup tables more compactly
(e.g. a table with the frequencies of each symbol could be just a
256-item list). But the memory gain is insignificant and there are
greater opportunities for bugs when symbols are represented in two
possible ways in the code. So instead we are slightly more wasteful
and use a dictionary (with floats indexed by bytes) to represent that
kind of table.

Note this Python gotcha: it doesn't help that "for s in bytesequence",
where isinstance(bytesequence, bytes), gives int values to s, instead
of the length-1 bytes value that a sensible person would expect (I
iterate over a sequence of BYTES and I get integers instead? Come
on...). Apparently PEP 467 proposes to fix this with "for s in
bytesequence.iterbytes()", where s would indeed take on a length-1
bytes value. But it had not been adopted by mainstream Python at the
time of writing this.
"""


# pylint: disable=invalid-name, misplaced-comparison-constant

import heapq
import bitstring  # see this class's docstring for where to get this


class HuffmanCode:

    """A HuffmanCode object is built, using the well-known greedy
    algorithm, out of a table of expected frequencies for the symbols
    we expect to deal with. Once the object is built, we may invoke
    its encode method on a sequence of bytes, returning an encoded
    (hopefully shorter) sequence of bytes; and we may invoke its
    decode method on a sequence of bytes previously encoded with it,
    recovering the original sequence.

    The HuffmanCode class includes helper utilities (as static
    methods) for adding and removing padding bits (to reversibly and
    economically transform a bitstring of arbitrary length into one
    that fits into an integral number of bytes) and for creating a
    table of occurrences or frequencies given a sequence of symbols.
    """

    def __init__(self, frequencyTable):
        """Take a frequency table (a 256-item dictionary of floats (that add
        up to 1), the floats indexed by all possible byte values,
        giving the expected relative frequencies of each byte in the
        inputs to be encoded. Generate the corresponding Huffman code
        as a PrefixTree (q.v.) and store it as self.tree, an internal
        data structure of this object.

        Note to the candidate: to make a frequency table from a string
        of symbols, you may use the makeOccurrencesTable and
        occurrences2frequencies methods in this class.
        """

    def encode(self, plaintextBytes):
        """Take a bytes object (immutable array of bytes) to be
        encoded. Encode it by replacing each of its bytes with the
        corresponding bitstring codeword, according to this object's
        Huffman code. Return a bitstring consisting of the
        concatenation of all these codewords, finished off with
        suitable padding (cfr paddingSuitableFor and removePadding
        methods).
        """

    def decode(self, encodedAndPaddedBits):
        """Take a bitstring to be decoded, consisting logically of a sequence
        of codewords followed by padding, but practically of an
        immutable bitstring, i.e. a sequence of bits without any
        delimiters to separate the variable-length codewords. Remove
        the padding and substitute each codeword with its
        corresponding byte symbol, according to this object's Huffman
        code. Return a bytearray with the decoded result.
        """

    def codewordFor(self, symbol):
        """Given a symbol (a single byte), return a bitstring with the
        codeword for that symbol.
        """

    @staticmethod
    def paddingSuitableFor(bits):
        """Take a bitstring of arbitrary length and return a short bitstring
        of padding, of length between 1 and 8 bits that, if appended
        to it, will make the total length a multiple of 8. This
        padding is reversible. It consists of a 1 and then as many 0s
        as necessary to reach the next multiple of 8.
        """

    @staticmethod
    def removePadding(bits):
        """Take a padded bitstring, whose length will be a multiple of
        8. Return a new (mutable) bitstring.BitStream obtained from
        the previous one by removing the padding (without changing the
        original). Take away all consecutive trailing 0s, if any, and
        then the first 1. The returned result will be 1 to 8 bits
        shorter than the input.
        """

    @staticmethod
    def makeOccurrencesTable(symbols):
        """Take a sequence of symbols (a bytes object in Python, i.e. an
        immutable array of bytes) and return a 256-item dictionary of
        non-negative integers, indexed by symbols (bytes), giving the
        number of occurrences of each byte in the given symbol
        sequence. NB: the dictionary will contain entries for all 256
        possible symbols (bytes), even if they don't all occur in the
        given sequence.
        """

    @staticmethod
    def occurrences2frequencies(occurrences):
        """Take a table of occurrences, as generated by the
        makeOccurrencesTable method. Return the corresponding table of
        frequencies (a 256-item dictionary of floats indexed by
        symbols) obtained by normalising the entries of the previous
        table so that they all add up to 1.0.

        Raise a ValueError exception if all the occurrences in the
        table were 0, because this makes normalisation impossible (in
        the sense that it makes it impossible for this routine to
        guarantee the "sum is 1" postcondition, so we refuse to
        operate on such degenerate tables).
        """
