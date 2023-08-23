#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fsa.py
# (c) Frank Stajano 2022-10-20 -- 2023-01-09
# $Id: fsa.py 53 2023-01-10 22:06:08Z fms27 $

"""Fixed-Size Array class for the algorithms tick."""


class FixedSizeArray:
    """Fixed-size array with basic accessors. No constraints on the type
    of the valued stored. No enforced consistency of homogeneity of
    type among the elements.
    """

    def __init__(self, n):
        """Take a natural number n and create a FixedSizeArray of that size,
        with all its elements initially set to None."""
        if isinstance(n, int):
            if n >= 0:
                self._n = n
                self._a = [None, ] * n
            else:
                raise ValueError(f"size must be >=0, not {n}")
        else:
            raise TypeError(f"size must be a natural number, not {n}")

    def __getitem__(self, index):
        """Return the value stored in the cell at the given index."""
        if self._isValidIndex(index):
            return self._a[index]
        else:
            raise IndexError(index)

    def __setitem__(self, index, value):
        """Write the supplied value into the cell at the given index."""
        if self._isValidIndex(index):
            self._a[index] = value
        else:
            raise IndexError(index)

    def __len__(self):
        """Return the number of cells in the array."""
        return self._n

    def __repr__(self):
        return repr(self._a)

    def __str__(self):
        return f"{self._n}-item fsa.FixedSizeArray: {repr(self)}"

    def _isValidIndex(self, n):
        return isinstance(n, int) and n >= 0 and n < self._n
