from huffman.huffman_node import HuffmanNode
from heapq import heappop, heappush
from huffman.binary_io import BinaryWriter

def build_freq_dict(filename):
    """
    calculates freq of each character in a file and store the result in a
    dictionary
    :param filename: input filename
    :return: freq dictionary (character: freq)
    """
    freq = {}
    with open(filename, "r") as f:
        for line in f:
            for c in line:
                freq[c] = freq[c] + 1 if c in freq else 1
    return freq


def build_min_heap(freq):
    """
    Build a min queue heap structure from the freq dictionary
    :param freq: dictionary
    :return: heap (list)
    """
    heap = []
    for char, freq in freq.items():
        node = HuffmanNode(char, freq)
        heappush(heap, node)
    return heap


def get_code_map(root):
    """
    returns the variable length code for each character in
    huffman binary tree
    :param root: of huffman binary tree
    :return: dictionary (character: code)
    """
    code_map = {}
    _calc_code(root, code_map)
    return code_map


def _calc_code(root, code_map, code=''):
    if not root.is_internal():
        code_map[root.character] = code
    else:
        if root.left is not None:
            _calc_code(root.left, code_map, code=code + '0')

        if root.right is not None:
            _calc_code(root.right, code_map, code=code + '1')



def build_huffman_tree(heap, freq):
    """
    build huffman code binary tree using huffman algorithm
    :param heap: heap of nodes
    :param freq: freq of characters
    :return: root of the tree
    """
    for i in range(len(freq.keys())):
        x = heappop(heap)
        y = heappop(heap) if len(heap) else None
        z = HuffmanNode(None, x.freq + y.freq, x, y) if y else x
        heappush(heap, z)
    return heappop(heap)

if __name__ == '__main__':
    file_name = './sample'

    # to keep freq of each character in the input file
    # read input file and calculate freq
    freq = build_freq_dict(file_name)

    # for each character build a huffman node and insert it
    # into the min queue
    heap = build_min_heap(freq)

    # build huffman tree and get root
    root = build_huffman_tree(heap, freq)

    # get variable length code for each character
    code_map = get_code_map(root)

    # TODO: print the header to the compressed file

    # print the code representation for each character to the compressed file
    # TODO: improve this print - python binary print is terrible
    with open(file_name + ".zipy", "wb") as output_file, open(file_name, "r") as input_file:
        bw = BinaryWriter(output_file, 8)
        for line in input_file:
            for c in line:
                for digit in code_map[c]:
                    bw.write(digit != '0')

