"""
Implements Data structures needed for construction of huffman code
binary tree
"""

from functools import total_ordering


@total_ordering
class HuffmanNode:
    """
    Class to represent nodes in the BT used to construct huffman code
    """
    def __init__(self, character, freq, left=None, right=None):
        self.character = character
        self.freq = freq
        self.left = left
        self.right = right

    def is_internal(self):
        """
        check whether a node is an internal huffman node or not
        :return: Boolean
        """
        return self.character is None

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, 'freq')

    def __eq__(self, other):
        if HuffmanNode._is_valid_operand(other):
            return self.freq == other.freq
        else:
            return NotImplemented

    def __lt__(self, other):
        if HuffmanNode._is_valid_operand(other):
            return self.freq < other.freq
        else:
            return NotImplemented
