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
        """
        min_heap = MinHeapOfPrefixTrees()
        for s, f in frequencyTable.items():
            curr_tree = PrefixTree(f, s)
            min_heap.push(curr_tree)

        while min_heap.size() > 1:
            t1 = min_heap.popMin()
            t2 = min_heap.popMin()
            min_heap.push(PrefixTree.fromTwoTrees(t1, t2))

        self.tree = min_heap.popMin()


        

    def encode(self, plaintextBytes):
        """Take a bytes object (immutable array of bytes) to be
        encoded. Encode it by replacing each of its bytes with the
        corresponding bitstring codeword, according to this object's
        Huffman code. Return a bitstring consisting of the
        concatenation of all these codewords, finished off with
        suitable padding (cfr paddingSuitableFor and removePadding
        methods).
        """
        codeword = bitstring.BitArray('0b0')
        for byte in plaintextBytes:
            codeword.append(self.codewordFor(byte.to_bytes(1, 'big')))
        
        del codeword[0]
        codeword.append(self.paddingSuitableFor(codeword))

        return codeword



    def decode(self, encodedAndPaddedBits):
        """Take a bitstring to be decoded, consisting logically of a sequence
        of codewords followed by padding, but practically of an
        immutable bitstring, i.e. a sequence of bits without any
        delimiters to separate the variable-length codewords. Remove
        the padding and substitute each codeword with its
        corresponding byte symbol, according to this object's Huffman
        code. Return a bytearray with the decoded result.
        """
        bits = self.removePadding(encodedAndPaddedBits)
        decoded = bytearray()
        t = self.tree
        for bit in bits:
            if not bit:
                t = t.left
            else:
                t = t.right
            if t.isSingleton():
                decoded.append(int.from_bytes(t.leaf, 'big'))
                t = self.tree
                continue
            

        return decoded

    def codewordFor(self, symbol):
        """Given a symbol (a single byte), return a bitstring with the
        codeword for that symbol.
        """
        def treeSearch(t, code):
            # If we find the correct symbol
            if t.isSingleton() and t.leaf == symbol:
                return code
            
            # If we haven't found a symbol
            if not t.isSingleton():
                try:
                    code.append('0b0')
                    left = treeSearch(t.left, code)
                    return left
                except WrongSymbolException:
                    try:
                        code[-1] = '0b1'
                        right = treeSearch(t.right, code)
                        return right
                    except WrongSymbolException:
                        del code[-1]
                        raise WrongSymbolException()

            # If we find the wrong symbol
            else:
                raise WrongSymbolException()

        codeword = treeSearch(self.tree, bitstring.BitArray('0b0'))
        # Remove extra 0 from start of codeword
        del codeword[0]
        return codeword

    @staticmethod
    def paddingSuitableFor(bits):
        """Take a bitstring of arbitrary length and return a short bitstring
        of padding, of length between 1 and 8 bits that, if appended
        to it, will make the total length a multiple of 8. This
        padding is reversible. It consists of a 1 and then as many 0s
        as necessary to reach the next multiple of 8.
        """
        length = 8 - len(bits) % 8 
        if length == 0:
            length += 8
        padding = bitstring.BitArray('0b1')
        length -= 1
        while length > 0:
            padding.append('0b0')
            length -= 1
  
        return padding 

    @staticmethod
    def removePadding(bits):
        """Take a padded bitstring, whose length will be a multiple of
        8. Return a new (mutable) bitstring.BitStream obtained from
        the previous one by removing the padding (without changing the
        original). Take away all consecutive trailing 0s, if any, and
        then the first 1. The returned result will be 1 to 8 bits
        shorter than the input.
        """
        bits = bitstring.BitStream(bits)
        while not bits[-1]:
            del bits[-1]
        del bits[-1]
        return bits


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
        occurence_table = {}
        for i in range(256):
            occurence_table[i.to_bytes(1, 'big')] = 0
        
        for s in symbols:
            occurence_table[s.to_bytes(1, 'big')] += 1
        
        return occurence_table
        
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
        total_symbols = sum(occurrences.values())
        if total_symbols == 0:
            raise ValueError
        else:
            for symbol in occurrences:
                occurrences[symbol] /= total_symbols
        return occurrences

       
class PrefixTree:
    """Prefix trees are used in the construction of the Huffman code. They
    are binary trees where each node has either zero or two
    children. The leaves contain symbols. The branches from parent to
    children are labelled zero and one. The sequence of branch labels
    from root to any leaf gives a bit string representing the codeword
    for that symbol, in the context of the given prefix tree.
    Because the algorithm for constructing a Huffman code manipulates
    a forest of these trees, repeatedly pairing up the emerging ones
    into a new tree, each tree has a key() method that gives its
    priority in the pecking order: the first trees to be picked for
    merging should be the ones with the lowest frequencies (where by
    "frequency" we mean the sum of the frequencies of all the leaves
    in the tree).
    Purely for reasons of comparability of student code with test
    harness code, we impose the additional constraint that, when two
    trees have the same aggregate frequency, the lower key should be
    that of the tree containing the lowest symbol. Since no symbol
    belongs to more than one tree, this makes the criterion
    unambiguous. We implement the criterion by suitably defining the
    key() method.
    This class has a basic constructor, __init__(), to build a
    (singleton) tree out of a symbol and its frequency, and a factory
    constructor, fromTwoTrees(), to build a tree by merging two
    existing trees.
    """
    

    def __init__(self, frequency, symbol=None):
        """Create a singleton tree with the supplied symbol as leaf."""
        self.root = frequency
        self.left = None
        self.right = None
        self.leaf = symbol

    # override the comparison operator
    def __lt__(self, nxt):
        s_freq, s_symb = self.key()
        n_freq, n_symb = nxt.key()
        if not s_freq == n_freq:
            return s_freq < n_freq
        else:
            return s_symb < n_symb
    
    def inorder(self, t):
        if t.isSingleton():
            return t.symbol
        self.inorder(t.left)
        self.inorder(t.right)


    def key(self):
        """Return the key for this tree. Lower key means higher priority. The
        priority is primarily determined by the aggregate frequency of
        all the leaves in the tree (lower frequency = lower key =
        higher priority). However, should two trees have the same
        aggregate frequency, the tie-breaker is the byte value of the
        lowest symbol in each tree (lower byte = lower key = higher
        priority).
        """
        if self.isSingleton():
            return (self.root, int.from_bytes(self.leaf, 'big'))
        
        min = 256
        def findMinSymbol(t, m):
            if t.isSingleton():
                leaf_val = int.from_bytes(t.leaf, 'big')
                return leaf_val if leaf_val < m else m
                
            m = findMinSymbol(t.left, m)
            m = findMinSymbol(t.right, m)
            return m
        
        min = findMinSymbol(self, min)

        return (self.root, min) 
    

    @staticmethod
    def fromTwoTrees(t1, t2):
        """Factory constructor to make a new PrefixTree out of two
        others. Return a new tree obtained by creating a new root and
        making the supplied trees its left and right children, with
        the left child being the tree with the lowest key.
        """
        t3 = PrefixTree(t1.key()[0] + t2.key()[0])
        t3.left = min(t1, t2)
        t3.right = max(t1, t2)
        return t3


    def isSingleton(self):
        """Return True iff the root of this tree has no children and thus
        contains a symbol."""
        return self.left == None and self.right == None 

class WrongSymbolException(Exception):
    """When searching for a symbol in a prefix tree we have found a symbol
    but it isn't the correct one
    """

class InvariantViolation(Exception):
    """We promised that a certain property would always hold but we found
    a case where it didn't.
    """


class MinHeapOfPrefixTrees:
    """A thin wrapper around the standard library's heapq to make it
    object oriented, so that we can create MinHeap objects and invoke
    methods on them.
    The items stored in this heap will be PrefixTree items,
    prioritised by their key method (lowest key = top item in the
    MinHeap). The PrefixTree.key method guarantees that no two
    PrefixTrees have the same key.
    """

    def __init__(self, unsortedTrees=None):
        """Create a min heap, optionally from a list of PrefixTrees."""
        if unsortedTrees != None:
            self.heap = heapq.heapify(unsortedTrees)
        else:
            self.heap = []


    def isEmpty(self):
        """Return true iff this min heap is empty."""
        return self.heap == []

    def push(self, t):
        """Push the given PrefixTree onto the min heap."""
        heapq.heappush(self.heap, t)

    def popMin(self):
        """Assuming this min heap is not empty, remove and return its
        smallest item (a PrefixTree)."""
        return heapq.heappop(self.heap)

    def size(self):
        """Return the number of items in the heap."""
        return len(self.heap)