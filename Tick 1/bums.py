#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bums.py
# (c) Frank Stajano 2020-01-19 -- 2022-11-27
# $Id: bums_template.py 53 2023-01-10 22:06:08Z fms27 $

# Copyright (c) <year>, <student author of the missing bits>

# This software was produced as an exercise for the Algorithms 1
# course at the University of Cambridge. Redistribution facilitates
# plagiarism and is not allowed. Reuse by the course lecturer is allowed.


"""Sort an n-item array using bottom-up mergesort. You are only given
enough scratch space to hold half of the original array (n/2 rounded
down, written as n//2).

The strategy must be to move the rightmost chunk into scratch space,
because the rightmost chunk, even at the top level, can never be
larger than half the array (whereas the leftmost chunk can: 9 cells
will split as 8+1 at the top level).
"""

import fsa


class Sorter:
    """Wrapper class for bottom-up merge sort.

    An object of this class is initialised with the data to be sorted
    and it creates an appropriate amount of scratch space. Sort the
    data by invoking the sort() method.
    """

    # --------------------------------------------------
    # METHODS TO BE IMPLEMENTED BY THE CANDIDATE

    def passes(self):
        """Return an integer denoting the number of passes that need to be
        made on the array in order to mergesort it bottom-up. Pass 0
        merges chunks of size up to 2^0; in general, pass i merges
        chunks of size up to 2^i. If the size of the data array is 8,
        3 passes are required (to merge chunks of size 1, 2 and
        4). For size 9, 4 passes would be required.
        """
        passes = 0
        length = len(self.d)
        for i in range(length):
            if 2**i >= length:
                passes = i
                break
        return passes

    def chunkSizeInPass(self, p):
        """Return an integer denoting the (maximum) size of a chunk during
        pass p, where passes are numbered from 0 as described in the
        docstring for the passes() method.

        PRECONDITION: p is an integer between 0 included and
        self.passes() excluded.
        """
        return 2**p

    def sort(self):
        """Sort the values in self.d in ascending order, leaving them in
        self.d, using the bottom-up merge sort algorithm, without
        using any sorting functions from Python or its library, using
        self.s as scratch space and without allocating any further
        memory to hold values from self.d.

        PRECONDITION: self.d is an fsa array of items to be sorted;
        self.s is another, which holds exactly as much scratch space
        as necessary. Both may be overwritten.

        POSTCONDITON self.d contains the same values as before, but
        sorted in ascending order.
        """
        num_passes = self.passes()
        l_arr = len(self.d)
        for i in range(num_passes):
            chunk = self.chunkSizeInPass(i)
            # Check it's not the last pass
            if i != num_passes-1:
                for j in range(0, l_arr, chunk*2):
                    # Check if only two chunks to sort
                    if l_arr-j-chunk*2 < 0:
                        if l_arr-j-chunk < 0:
                            break
                        else:
                            # Copy chunk into scratch space
                            Sorter.lddr(
                                self.d, l_arr-j-chunk, l_arr-j,
                                self.s, 0, chunk)
                            # Merge chunks
                            self.mergeRL(
                                self.d, 0, l_arr-j-chunk,
                                self.s, 0, chunk,
                                self.d, 0, l_arr-j)
                    else:
                        # Copy chunk into scratch space
                        Sorter.lddr(self.d, l_arr-j-chunk, l_arr-j,
                                    self.s, 0, chunk)
                        # Merge chunks
                        self.mergeRL(self.d, l_arr-j-chunk*2, l_arr-j-chunk,
                                     self.s, 0, chunk,
                                     self.d, l_arr-j-chunk*2, l_arr-j)

            # If it is the last pass
            else:
                # Copy chunk into scratch space
                Sorter.lddr(self.d, 0, l_arr-chunk,
                            self.s, 0, l_arr-chunk)
                # Move array to the left
                Sorter.lddr(self.d, l_arr-chunk, l_arr,
                            self.d, 0, chunk)
                # Merge chunks
                self.mergeRL(self.d, 0, chunk,
                             self.s, 0, l_arr-chunk,
                             self.d, 0, l_arr)

    def mergeRL(
            self,
            arraySrc1, iStartSrc1, iEndSrc1,  # src1
            arraySrc2, iStartSrc2, iEndSrc2,  # src2
            arrayDst, iStartDst, iEndDst,  # dst
            ):
        """Merge the array regions arraySrc1[iStartSrc1:iEndSrc1] and
        arraySrc2[iStartSrc2:iEndSrc2], putting the result in
        arrayDst[iStartDst:iEndDst] (NB we use python slice notation,
        left end included and right end excluded, even though it does
        not work on the homemade arrays from the supplied fsa module.)
        Proceed right to left in all three arrays.

        PRECONDITION:

        1) The source regions arraySrc1[iStartSrc1:iEndSrc1] and
        arraySrc2[iStartSrc2:iEndSrc2] are already sorted in ascending
        order.

        2) The sum of the sizes of the two sources is equal to the
        size of the destination.

        3) The caller guarantees that proceeding right to left in all
        three arrays will not overwrite any of the source values.

        POSTCONDITION: the destination region
        arrayDst[iStartDst:iEndDst] is sorted in ascending order.
        """
        p1 = iEndSrc1-1
        p2 = iEndSrc2-1
        for i in range(iEndDst-iStartDst):
            # Check if one of the subarrays has already been fully used
            if p1 < iStartSrc1:
                Sorter.lddr(arraySrc2, iStartSrc2, p2+1,
                            arrayDst, iStartDst, iEndDst-1-i)
                break
            elif p2 < iStartSrc2:
                Sorter.lddr(arraySrc1, iStartSrc1, p1+1,
                            arrayDst, iStartDst, iEndDst-1-i)
                break
            # Get min of two current positions in subarray
            # And put into destination array
            if arraySrc1[p1] > arraySrc2[p2]:
                arrayDst[iEndDst-1-i] = arraySrc1[p1]
                p1 -= 1
            else:
                arrayDst[iEndDst-1-i] = arraySrc2[p2]
                p2 -= 1

    @staticmethod
    def lddr(arraySrc, iStartSrc, iEndSrc, arrayDst, iStartDst, iEndDst):
        """Copy the source block arraySrc[iStartSrc:iEndSrc] to the
        destination area arrayDst[iStartDst:iEndDst]. The blocks must
        be of the same size. The blocks may or may not be in the same
        array. If they are in the same array, they may be identical
        (in which case this function call is a no-operation) or they
        may overlap provided that iEndDst > iEndSrc. The name of this
        method is inspired by the Z80 assembly language block copy
        instruction LDDR, which stood for "load, decrement, repeat".

        PRECONDITION:

        0) arraySrc and arrayDst are fsa.FixesSizeArray, whereas the i
        parameters are integer indices into them.

        1) source and destination regions have same size.

        2) either they are the same, they don't overlap or the source
        comes first.

        POSTCONDITION:

        The destination region contains the same values that the
        source region did, in the same order. If the regions didn't
        overlap, the source sregion is unchanged.
        """
        if (arraySrc != arrayDst) | (iEndSrc >= iEndDst):
            for i in range(iEndSrc-iStartSrc):
                arrayDst[iStartDst+i] = arraySrc[iStartSrc+i]
        else:
            for i in range(iEndSrc-iStartSrc):
                arrayDst[iEndDst-1-i] = arraySrc[iEndSrc-1-i]

    # --------------------------------------------------
    # ALREADY-WRITTEN METHODS. DO NOT EDIT

    def __init__(self, dataArray):
        """Create a Sorter instance from an fsa array with the items to be
        sorted, allocating the correct amount of scratch space for it.
        """
        self.d = dataArray
        self.s = fsa.FixedSizeArray(len(dataArray) // 2)
