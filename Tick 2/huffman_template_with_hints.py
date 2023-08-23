#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# huffman.py
# (c) Frank Stajano 2022-12-14
# $Id: huffman_template_with_hints.py 70 2023-02-03 15:50:45Z fms27 $


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

""" byte = b'aabbccc'
occ_table = HuffmanCode.makeOccurrencesTable(byte)
freq_table = HuffmanCode.occurrences2frequencies(occ_table)
huff = HuffmanCode(freq_table)
codeword = huff.encode('hello there!')
print(f' codeword: {codeword}')
word = huff.decode(codeword)
print(f'word: {word}')

def ha(b):
    if b == '0b00000':
        print(b)
        return b
    b.append('0b0')
    ha(b)
bits = bitstring.BitArray('0b010100')
bits.append('0b10')
print(bits.bin) """

byte = b'aaabhellloo'
occ_table = HuffmanCode.makeOccurrencesTable(byte)
freq_table = HuffmanCode.occurrences2frequencies(occ_table)
huff = HuffmanCode(freq_table)
print(huff.tree)
codeword = huff.encode('what the cunt has this worked?')
print(huff.decode(codeword))

# Note from FMS to candidate: In my own solution I also wrote the
# following classes. You are not required to do so, but I leave this stuff
# in here in case it gives you any useful ideas.


# class PrefixTree:

#     """Prefix trees are used in the construction of the Huffman code. They
#     are binary trees where each node has either zero or two
#     children. The leaves contain symbols. The branches from parent to
#     children are labelled zero and one. The sequence of branch labels
#     from root to any leaf gives a bit string representing the codeword
#     for that symbol, in the context of the given prefix tree.

#     Because the algorithm for constructing a Huffman code manipulates
#     a forest of these trees, repeatedly pairing up the emerging ones
#     into a new tree, each tree has a key() method that gives its
#     priority in the pecking order: the first trees to be picked for
#     merging should be the ones with the lowest frequencies (where by
#     "frequency" we mean the sum of the frequencies of all the leaves
#     in the tree).

#     Purely for reasons of comparability of student code with test
#     harness code, we impose the additional constraint that, when two
#     trees have the same aggregate frequency, the lower key should be
#     that of the tree containing the lowest symbol. Since no symbol
#     belongs to more than one tree, this makes the criterion
#     unambiguous. We implement the criterion by suitably defining the
#     key() method.

#     This class has a basic constructor, __init__(), to build a
#     (singleton) tree out of a symbol and its frequency, and a factory
#     constructor, fromTwoTrees(), to build a tree by merging two
#     existing trees.
#     """

#     def __init__(self, symbol, frequency):
#         """Create a singleton tree with the supplied symbol as leaf."""

#     def key(self):
#         """Return the key for this tree. Lower key means higher priority. The
#         priority is primarily determined by the aggregate frequency of
#         all the leaves in the tree (lower frequency = lower key =
#         higher priority). However, should two trees have the same
#         aggregate frequency, the tie-breaker is the byte value of the
#         lowest symbol in each tree (lower byte = lower key = higher
#         priority).
#         """

#     @staticmethod
#     def fromTwoTrees(t1, t2):
#         """Factory constructor to make a new PrefixTree out of two
#         others. Return a new tree obtained by creating a new root and
#         making the supplied trees its left and right children, with
#         the left child being the tree with the lowest key.
#         """

#     def isSingleton(self):
#         """Return True iff the root of this tree has no children and thus
#         contains a symbol."""


# class InvariantViolation(Exception):
#     """We promised that a certain property would always hold but we found
#     a case where it didn't.
#     """


# class MinHeapOfPrefixTrees:

#     """A thin wrapper around the standard library's heapq to make it
#     object oriented, so that we can create MinHeap objects and invoke
#     methods on them.

#     The items stored in this heap will be PrefixTree items,
#     prioritised by their key method (lowest key = top item in the
#     MinHeap). The PrefixTree.key method guarantees that no two
#     PrefixTrees have the same key.
#     """

#     def __init__(self, unsortedTrees=None):
#         """Create a min heap, optionally from a list of PrefixTrees."""

#     def isEmpty(self):
#         """Return true iff this min heap is empty."""

#     def push(self, t):
#         """Push the given PrefixTree onto the min heap."""

#     def popMin(self):
#         """Assuming this min heap is not empty, remove and return its
#         smallest item (a PrefixTree)."""

#     def size(self):
#         """Return the number of items in the heap."""
